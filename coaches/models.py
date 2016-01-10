from django.core.mail import EmailMessage
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from core.models import EventPage, User
from .utils import DEFAULT_QUESTIONS

QUESTION_TYPES = (
    ('paragraph', 'Paragraph'),
    ('text', 'Long text'),
    ('choices', 'Choices'),
    ('email', 'Email')
)

APPLICATION_STATES = (
    ('submitted', 'Coach form submitted'),
    ('accepted', 'Registration accepted'),
    ('rejected', 'Registration rejected'),
)


@python_2_unicode_compatible
class CoachForm(models.Model):
    page = models.ForeignKey(EventPage, null=False, blank=False)
    text_header = models.CharField(
        max_length=255, default="Register to be a coach at Django Girls [City]!")
    text_description = models.TextField(
        default="First of all: if you're reading this, that means you've decided to help us out "
                "during Django Girls workshop. You rock! Thank you :) \n\n"
                "We're doing this quick survey to gather all the information about coaches in one place, "
                "to get to know you better and make sure we can find a group of learners "
                "who will be the best match for you.\n\n"
                "You can find the coaching manual <a href=\"http://coach.djangogirls.org/\">here</a>.")
    confirmation_mail = models.TextField(
        default="Hi there!"
                "This is a confirmation of your registering to coach at "
                "<a href=\"http://djangogirls.org/{city}\">Django Girls {CITY}</a>. "
                "Yay! Thank you so much!\n\n"

                "You'll receive an email from the team that organizes Django Girls {CITY} soon. "
                "You can always reach them by answering to this email or by writing to {your event mail}.\n"
                "For your reference, we're attaching your answers below.\n\n"
                "Hugs, rainbows and sparkles!\n"
                "Django Girls",
        help_text="Mail will be sent from your event mail.\nAlso the answers will be attached.")
    open_from = models.DateTimeField(
        null=True, verbose_name="Coach application process is open from")
    open_until = models.DateTimeField(
        null=True, verbose_name="Coach application process is open until")

    def __str__(self):
        return 'Coach registration form for {}'.format(self.page.event.name)

    def save(self, *args, **kwargs):
        is_form_new = False if self.pk else True
        super(CoachForm, self).save(*args, **kwargs)

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
        # TODO: fix
        return self.coachapplication_set.count()

    @property
    def coach_application_open(self):
        if self.open_from and self.open_until:
            return self.open_from < timezone.now() < self.open_until
        return True


@python_2_unicode_compatible
class Question(models.Model):
    form = models.ForeignKey(CoachForm, null=False, blank=False)
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

    def __str__(self):
        return self.title

    def get_choices_as_list(self):
        if self.question_type != 'choices':
            raise TypeError(
                "You can only get choices for fields that have"
                " question_type == choices."
            )

        return self.choices.split(';')


@python_2_unicode_compatible
class CoachApplication(models.Model):
    form = models.ForeignKey(CoachForm, null=False, blank=False)
    number = models.PositiveIntegerField(default=1, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(
        max_length=50,
        choices=APPLICATION_STATES, verbose_name="State of the coach application",
        null=True,
        default='submitted'
    )
    email = models.EmailField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.number = CoachApplication.objects.filter(form=self.form).count() + 1
        super(CoachApplication, self).save(*args, **kwargs)

    @property
    def is_accepted(self):
        return self.state == 'accepted'

    def __str__(self):
        return str(self.pk)


class Answer(models.Model):
    application = models.ForeignKey(CoachApplication, null=False, blank=False)
    question = models.ForeignKey(Question, null=False, blank=False)
    answer = models.TextField()

    class Meta:
        ordering = ('question__order',)


@python_2_unicode_compatible
class CoachEmail(models.Model):
    form = models.ForeignKey(CoachForm)
    author = models.ForeignKey(User, related_name="email_author")
    subject = models.CharField(max_length=255)
    text = models.TextField(
        verbose_name="Content of the email",
        help_text="You can use HTML syntax in this message. Preview on the right."
    )
    recipients_group = models.CharField(
        max_length=50, choices=APPLICATION_STATES,
        verbose_name="Recipients",
        help_text="Only people assigned to chosen group will receive this email."
    )
    number_of_recipients = models.IntegerField(default=0, null=True)
    successfully_sent = models.TextField(null=True, blank=True)
    failed_to_sent = models.TextField(null=True, blank=True)
    sent_from = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

    def get_coach_applications(self):
        application_states = [x[0] for x in APPLICATION_STATES]
        if self.recipients_group in application_states:
            return CoachApplication.objects.filter(form=self.form, state=self.recipients_group)
        else:
            return CoachApplication.objects.none()

    def send(self):
        recipients = self.get_coach_applications()
        self.number_of_recipients = recipients.count()
        self.sent_from = self.form.page.event.email or '{}@djangogirls.org'.format(self.form.page.url)
        successfully_sent = []
        failed_to_sent = []

        for recipient in recipients:
            if recipient.email:
                body = self.text.replace('\n', '<br />')
                msg = EmailMessage(self.subject, body, self.sent_from, [recipient.email])
                msg.content_subtype = "html"
                try:
                    msg.send()
                    successfully_sent.append(recipient.email)
                except:
                    failed_to_sent.append(recipient.email)

        self.sent = timezone.now()
        self.successfully_sent = ', '.join(successfully_sent)
        self.failed_to_sent = ', '.join(failed_to_sent)
        self.save()
