import random
import string

from django.core.mail import EmailMessage
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import Event, User

from .questions import DEFAULT_QUESTIONS

RSVP_LINKS = ["[rsvp-url-yes]", "[rsvp-url-no]"]


class Form(models.Model):
    event = models.OneToOneField(Event, on_delete=models.deletion.CASCADE)
    text_header = models.CharField(max_length=255, default=_("Apply for a spot at Django Girls [City]!"))
    text_description = models.TextField(
        default=_(
            "Yay! We're so excited you want to be a part of our "
            "workshop. Please mind that filling out the form below does "
            "not give you a place on the workshop, but a chance to get "
            "one. The application process is open from {INSERT DATE} "
            "until {INSERT DATE}. If you're curious about the criteria "
            "we use to choose applicants, you can read about it on "
            "<a href='http://blog.djangogirls.org/post/91067112853/"
            "djangogirls-how-we-scored-applications'>Django Girls "
            "blog</a>. Good luck!"
        )
    )
    confirmation_mail = models.TextField(
        default=_(
            "Hi there!\n\n"
            'This is a confirmation of your application to <a href="http://djangogirls.org/{city}">'
            "Django Girls {CITY}</a>. "
            "Yay! That's a huge step already, we're proud of you!\n\n"
            "Mind that this is not a confirmation of participation in the event, but a confirmation that we received "
            "your application.\n\n"
            "You'll receive an email from the team that organizes Django Girls {CITY} soon. "
            "You can always reach them by answering to this email or by writing to {your event mail}.\n"
            "For your reference, we're attaching your answers below.\n\n"
            "Hugs, cupcakes and high-fives!\n"
            "Django Girls"
        ),
        help_text="Mail will be sent from your event mail.\nAlso the answers will be attached.",
    )
    open_from = models.DateTimeField(null=True, verbose_name=_("Application process is open from"))
    open_until = models.DateTimeField(null=True, verbose_name=_("Application process is open until"))

    def __str__(self):
        return f"Application form for {self.event.name}"

    def save(self, *args, **kwargs):
        is_form_new = False if self.pk else True
        super().save(*args, **kwargs)

        if is_form_new:
            self.create_default_questions()

    def create_default_questions(self):
        i = 1
        for question in DEFAULT_QUESTIONS:
            question["form"] = self
            question["order"] = i
            Question.objects.create(**question)
            i += 1

    @property
    def number_of_applications(self):
        return self.application_set.count()

    @property
    def application_open(self):
        if self.open_from and self.open_until:
            return self.open_from < timezone.now() < self.open_until
        return True


class Question(models.Model):
    TEXT = "text"
    QUESTION_TYPES = (("paragraph", "Paragraph"), (TEXT, "Long text"), ("choices", "Choices"), ("email", "Email"))

    form = models.ForeignKey(to=Form, null=False, blank=False, on_delete=models.deletion.CASCADE)
    title = models.TextField(verbose_name=_("Question"))
    help_text = models.TextField(blank=True, default="", verbose_name=_("Additional help text to the question?"))
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES, verbose_name=_("Type of the question"))
    is_required = models.BooleanField(default=True, verbose_name=_("Is the answer to the question required?"))
    choices = models.TextField(
        blank=True,
        default="",
        verbose_name=_("List all available options, separated with semicolon (;)"),
        help_text=_("Used only with 'Choices' question type"),
    )
    is_multiple_choice = models.BooleanField(
        default=False,
        verbose_name=_("Are there multiple choices allowed?"),
        help_text=_("Used only with 'Choices' question type"),
    )
    order = models.PositiveIntegerField(help_text=_("Position of the question"))

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

    def get_choices_as_list(self):
        if self.question_type != "choices":
            raise TypeError(_("You can only get choices for fields that have" " question_type == choices."))

        return self.choices.split(";")


class Application(models.Model):
    APPLICATION_STATES = (
        ("submitted", _("Application submitted")),
        ("accepted", _("Application accepted")),
        ("rejected", _("Application rejected")),
        ("waitlisted", _("Application on waiting list")),
        ("declined", _("Applicant declined")),
    )
    RSVP_WAITING = "waiting"
    RSVP_YES = "yes"
    RSVP_NO = "no"

    RSVP_STATUSES = (
        (RSVP_WAITING, _("RSVP: Waiting for response")),
        (RSVP_YES, _("RSVP: Confirmed attendance")),
        (RSVP_NO, _("RSVP: Rejected invitation")),
    )

    form = models.ForeignKey(Form, null=False, blank=False, on_delete=models.deletion.CASCADE)
    number = models.PositiveIntegerField(default=1, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(
        verbose_name=_("State of the application"),
        max_length=50,
        choices=APPLICATION_STATES,
        null=True,
        default="submitted",
    )
    email = models.EmailField(null=True, blank=True)
    newsletter_optin = models.BooleanField(default=False)

    rsvp_status = models.CharField(
        max_length=50, choices=RSVP_STATUSES, verbose_name=_("RSVP status"), default=RSVP_WAITING
    )
    rsvp_yes_code = models.CharField(max_length=24, null=True, blank=True)
    rsvp_no_code = models.CharField(max_length=24, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["form", "email"],
                condition=models.Q(email__isnull=False),
                name="unique_form_email_email_not_null",
            )
        ]

    def save(self, *args, **kwargs):
        if self.pk is None:
            current_max = Application.objects.filter(form=self.form).aggregate(models.Max("number"))["number__max"]
            self.number = (current_max or 0) + 1
        super().save(*args, **kwargs)

    @property
    def average_score(self):
        """
        Return the average score for this Application.
        """
        scores = [s.score for s in self.scores.all() if (s.score and s.score > 0)]
        if not scores:
            return 0
        else:
            return sum(scores) / float(len(scores))

    def variance(self):
        data = [s.score for s in self.scores.all() if s.score]
        n = len(data)
        if n == 0:
            return 0
        c = sum(data) / float(len(data))
        if n < 2:
            return 0
        ss = sum((x - c) ** 2 for x in data)
        ss -= sum((x - c) for x in data) ** 2 / len(data)
        assert not ss < 0, "negative sum of square deviations: %f" % ss
        return ss / (n - 1)

    def stdev(self):
        return self.variance() ** 0.5

    def generate_code(self):
        return "".join([random.choice(string.ascii_letters + string.digits) for i in range(24)])

    def get_rsvp_yes_code(self):
        if not self.rsvp_yes_code:
            self.rsvp_yes_code = self.generate_code()
            self.save()
        return self.rsvp_yes_code

    def get_rsvp_no_code(self):
        if not self.rsvp_no_code:
            self.rsvp_no_code = self.generate_code()
            self.save()
        return self.rsvp_no_code

    @classmethod
    def get_by_rsvp_code(cls, code, event):
        """Returns application and RSVP status or None"""
        try:
            application = cls.objects.get(rsvp_yes_code=code, form__event=event)
            return application, Application.RSVP_YES
        except cls.DoesNotExist:
            try:
                application = cls.objects.get(rsvp_no_code=code, form__event=event)
                return application, Application.RSVP_NO
            except cls.DoesNotExist:
                return None, None

    @property
    def is_accepted(self):
        return self.state == "accepted"

    def is_scored_by_user(self, user):
        """
        Returns true if the given user has scored this application
        or false if they have not, or there is a zero score.
        """
        return self.scores.filter(user=user, score__gt=0).exists()

    def __str__(self):
        return str(self.pk)


class Answer(models.Model):
    application = models.ForeignKey(Application, null=False, blank=False, on_delete=models.deletion.PROTECT)
    question = models.ForeignKey(Question, null=False, blank=False, on_delete=models.deletion.PROTECT)
    answer = models.TextField()

    class Meta:
        ordering = ("question__order",)


class Score(models.Model):
    """
    A score represents the score given by a coach for an application.
    """

    user = models.ForeignKey(User, related_name="scores", on_delete=models.deletion.PROTECT)
    application = models.ForeignKey(Application, related_name="scores", on_delete=models.deletion.PROTECT)
    score = models.FloatField(
        help_text=_("5 being the most positive, 1 being the most negative."),
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        default=0,
    )
    comment = models.TextField(null=True, blank=True, help_text=_("Any extra comments?"))

    class Meta:
        unique_together = (
            "user",
            "application",
        )


class Email(models.Model):
    form = models.ForeignKey(Form, on_delete=models.deletion.PROTECT)
    author = models.ForeignKey(User, related_name="author", on_delete=models.deletion.PROTECT)
    subject = models.CharField(max_length=255)
    text = models.TextField(
        verbose_name=_("Content of the email"),
        help_text=_("You can use HTML syntax in this message. Preview on the right."),
    )
    recipients_group = models.CharField(
        max_length=50,
        choices=Application.APPLICATION_STATES + Application.RSVP_STATUSES,
        verbose_name=_("Recipients"),
        help_text=_("Only people assigned to chosen group will receive this email."),
    )
    number_of_recipients = models.IntegerField(default=0, null=True)
    successfuly_sent = models.TextField(null=True, blank=True)
    failed_to_sent = models.TextField(null=True, blank=True)
    sent_from = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

    def get_rsvp_link(self, code):
        return f"http://djangogirls.org/{self.form.event.page_url}/rsvp/{code}"

    def add_rsvp_links(self, body, application):
        body = body.replace("[rsvp-url-yes]", self.get_rsvp_link(application.get_rsvp_yes_code()))
        body = body.replace("[rsvp-url-no]", self.get_rsvp_link(application.get_rsvp_no_code()))
        return body

    def get_applications(self):
        application_states = [x[0] for x in Application.APPLICATION_STATES]
        rsvp_statuses = [x[0] for x in Application.RSVP_STATUSES]

        if self.recipients_group in application_states:
            return Application.objects.filter(form=self.form, state=self.recipients_group)
        elif self.recipients_group in rsvp_statuses:
            return Application.objects.filter(form=self.form, state="accepted", rsvp_status=self.recipients_group)
        else:
            return Application.objects.none()

    def send(self):
        recipients = self.get_applications()
        self.number_of_recipients = recipients.count()
        self.sent_from = self.form.event.email or f"{self.form.event.page_url}@djangogirls.org"
        successfuly_sent = []
        failed_to_sent = []

        for recipient in recipients:
            if recipient.email:
                body = self.text.replace("\n", "<br />")

                for rsvp_link in RSVP_LINKS:
                    if rsvp_link in body:
                        body = self.add_rsvp_links(body, recipient)
                        break

                msg = EmailMessage(self.subject, body, self.sent_from, [recipient.email])
                msg.content_subtype = "html"
                try:
                    msg.send()
                    successfuly_sent.append(recipient.email)
                except:  # TODO: What's the possible exception here? Catch specifics
                    failed_to_sent.append(recipient.email)

        self.sent = timezone.now()
        self.successfuly_sent = ", ".join(successfuly_sent)
        self.failed_to_sent = ", ".join(failed_to_sent)
        self.save()
