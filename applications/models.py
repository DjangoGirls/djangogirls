import random
import string

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.mail import EmailMessage
from django.db import models
from django.utils import timezone

from core.models import EventPage, User
from .utils import DEFAULT_QUESTIONS


QUESTION_TYPES = (
    ('paragraph', 'Paragraph'),
    ('text', 'Long text'),
    ('choices', 'Choices'),
    ('email', 'Email')
)

APPLICATION_STATES = (
    ('submitted', 'Application submitted'),
    ('accepted', 'Application accepted'),
    ('rejected', 'Application rejected'),
    ('waitlisted', 'Application on waiting list'),
)

RSVP_STATUSES = (
    ('waiting', 'RSVP: Waiting for response'),
    ('yes', 'RSVP: Confirmed attendance'),
    ('no', 'RSVP: Rejected invitation')

)

RSVP_LINKS = ['[rsvp-url-yes]', '[rsvp-url-no]']


class Form(models.Model):
    page = models.ForeignKey(EventPage, null=False, blank=False)
    text_header = models.CharField(
        max_length=255, default="Apply for a spot at Django Girls [City]!")
    text_description = models.TextField(
        default="Yay! We're so excited you want to be a part of our "
        "workshop. Please mind that filling out the form below does "
        "not give you a place on the workshop, but a chance to get "
        "one. The application process is open from {INSERT DATE} "
        "until {INSERT DATE}. If you're curious about the criteria "
        "we use to choose applicants, you can read about it on "
        "<a href='http://blog.djangogirls.org/post/91067112853/"
        "djangogirls-how-we-scored-applications'>Django Girls "
        "blog</a>. Good luck!")
    confirmation_mail = models.TextField(
        default="Hi there!"
        "This is a confirmation of your application to <a href=\"http://djangogirls.org/{city}\">Django Girls {CITY}</a>. "
        "Yay! That's a huge step already, we're proud of you!\n\n"
        "Mind that this is not a confirmation of participation in the event, but a confirmation that we received your application.\n\n"
        "You'll receive an email from the team that organizes Django Girls {CITY} soon. "
        "You can always reach them by answering to this email or by writing to {your event mail}.\n"
        "For your reference, we're attaching your answers below.\n\n"
        "Hugs, cupcakes and high-fives!\n"
        "Django Girls",
        help_text="Mail will be sent from your event mail.\nAlso the answers will be attached.")
    open_from = models.DateTimeField(
        null=True, verbose_name="Application process is open from")
    open_until = models.DateTimeField(
        null=True, verbose_name="Application process is open until")

    def __unicode__(self):
        return 'Application form for {}'.format(self.page.event.name)

    def save(self, *args, **kwargs):
        is_form_new = False if self.pk else True
        super(Form, self).save(*args, **kwargs)

        if is_form_new:
            self.create_default_questions()

    def create_default_questions(self):
        i = 1
        for question in DEFAULT_QUESTIONS:
            question['form'] = self
            question['order'] = i
            Question.objects.create(**question)
            i += 1

    @property
    def number_of_applications(self):
        return self.application_set.count()

    @property
    def application_open(self):
        if self.open_from and self.open_until:
            return (self.open_from < timezone.now() < self.open_until)
        return True


class Question(models.Model):
    form = models.ForeignKey(Form, null=False, blank=False)
    title = models.TextField(verbose_name="Question")
    help_text = models.TextField(
        blank=True, default='', verbose_name="Additional help text to the question?")
    question_type = models.CharField(
        max_length=50,
        choices=QUESTION_TYPES, verbose_name="Type of the question")
    is_required = models.BooleanField(
        default=True, verbose_name="Is the answer to the question required?")
    choices = models.TextField(
        blank=True, default='', verbose_name="List all available options, separated with semicolon (;)",
        help_text="Used only with 'Choices' question type")
    is_multiple_choice = models.BooleanField(
        default=False, verbose_name="Are there multiple choices allowed?",
        help_text="Used only with 'Choices' question type")
    order = models.PositiveIntegerField(
        null=False, blank=False, help_text="Position of the question")

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.title

    def get_choices_as_list(self):
        if self.question_type != 'choices':
            raise TypeError(
                "You can only get choices for fields that have"
                " question_type == choices."
            )

        return self.choices.split(';')


class Application(models.Model):
    form = models.ForeignKey(Form, null=False, blank=False)
    number = models.PositiveIntegerField(default=1, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(
        max_length=50,
        choices=APPLICATION_STATES, verbose_name="State of the application",
        null=True,
        default='submitted'
    )
    email = models.EmailField(null=True, blank=True)
    newsletter_optin = models.BooleanField(default=False)

    rsvp_status = models.CharField(
        max_length=50,
        choices=RSVP_STATUSES, verbose_name="RSVP status",
        default='waiting'
    )
    rsvp_yes_code = models.CharField(max_length=24, null=True)
    rsvp_no_code = models.CharField(max_length=24, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.number = Application.objects.filter(form=self.form).count() + 1
        super(Application, self).save(*args, **kwargs)

    @property
    def average_score(self):
        """
        Return the average score for this Application.
        """
        scores = [s.score for s in self.scores.all() if s.score]
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
        ss = sum((x-c)**2 for x in data)
        ss -= sum((x-c) for x in data)**2/len(data)
        assert not ss < 0, 'negative sum of square deviations: %f' % ss
        return ss / (n-1)

    def stdev(self):
        return self.variance() ** 0.5

    def generate_code(self):
        return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(24)])

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
    def get_by_rsvp_code(self, code, page):
        """ Returns application and RSVP status or None """
        try:
            application = self.objects.get(rsvp_yes_code=code, form__page=page)
            return application, 'yes'
        except self.DoesNotExist:
            try:
                application = self.objects.get(rsvp_no_code=code, form__page=page)
                return application, 'no'
            except self.DoesNotExist:
                return None
        return None

    @property
    def is_accepted(self):
        return self.state == 'accepted'

    def __unicode__(self):
        return str(self.pk)


class Answer(models.Model):
    application = models.ForeignKey(Application, null=False, blank=False)
    question = models.ForeignKey(Question, null=False, blank=False)
    answer = models.TextField()

    class Meta:
        ordering = ('question__order',)


class Score(models.Model):
    """
    A score represents the score given by a coach for an application.
    """

    user = models.ForeignKey(User, related_name='scores')
    application = models.ForeignKey(Application, related_name='scores')
    score = models.FloatField(
        null=True, blank=True,
        help_text='5 being the most positive, 1 being the most negative.',
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    comment = models.TextField(
        null=True, blank=True, help_text='Any extra comments?')

    class Meta:
        unique_together = ('user', 'application',)


class Email(models.Model):
    form = models.ForeignKey(Form)
    author = models.ForeignKey(User, related_name="author")
    subject = models.CharField(max_length=255)
    text = models.TextField(
        verbose_name="Content of the email",
        help_text="You can use HTML syntax in this message. Preview on the right."
    )
    recipients_group = models.CharField(
        max_length=50, choices=APPLICATION_STATES+RSVP_STATUSES,
        verbose_name="Recipients",
        help_text="Only people assigned to chosen group will receive this email."
    )
    number_of_recipients = models.IntegerField(default=0, null=True)
    successfuly_sent = models.TextField(null=True, blank=True)
    failed_to_sent = models.TextField(null=True, blank=True)
    sent_from = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(null=True, blank=True)

    def get_rsvp_link(self, code):
        return 'http://djangogirls.org/{}/rsvp/{}'.format(self.form.page.url, code)

    def add_rsvp_links(self, body, application):
        body = body.replace('[rsvp-url-yes]', self.get_rsvp_link(application.get_rsvp_yes_code()))
        body = body.replace('[rsvp-url-no]', self.get_rsvp_link(application.get_rsvp_no_code()))
        return body

    def get_applications(self):
        application_states = [x[0] for x in APPLICATION_STATES]
        rsvp_statuses = [x[0] for x in RSVP_STATUSES]

        if self.recipients_group in application_states:
            return Application.objects.filter(form=self.form, state=self.recipients_group)
        elif self.recipients_group in rsvp_statuses:
            return Application.objects.filter(form=self.form, state='accepted', rsvp_status=self.recipients_group)
        else:
            return Application.objects.none()

    def send(self):
        recipients = self.get_applications()
        self.number_of_recipients = recipients.count()
        self.sent_from = self.form.page.event.email or '{}@djangogirls.org'.format(self.form.page.url)
        sender = "{} <{}>".format(self.form.page.title, self.sent_from)
        successfuly_sent = []
        failed_to_sent = []

        for recipient in recipients:
            if recipient.email:
                body = self.text.replace('\n', '<br />')

                for rsvp_link in RSVP_LINKS:
                    if rsvp_link in body:
                        body = self.add_rsvp_links(body, recipient)
                        break

                msg = EmailMessage(self.subject, body, sender, [recipient.email])
                msg.content_subtype = "html"
                try:
                    msg.send()
                    successfuly_sent.append(recipient.email)
                except:
                    failed_to_sent.append(recipient.email)

        self.sent = timezone.now()
        self.successfuly_sent = ', '.join(successfuly_sent)
        self.failed_to_sent = ', '.join(failed_to_sent)
        self.save()
