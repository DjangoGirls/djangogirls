from django.db import models

from core.models import EventPage
from .utils import DEFAULT_QUESTIONS


QUESTION_TYPES = (
    ('paragraph', 'Paragraph'),
    ('text', 'Long text'),
    ('choices', 'Choices'),
    ('email', 'Email')
)

APPLICATION_STATES = (
    (0, 'Submitted'),
    (1, 'Accepted'),
    (2, 'Rejected'),
)


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


class Question(models.Model):
    form = models.ForeignKey(Form, null=False, blank=False)
    title = models.CharField(max_length=255, verbose_name="Question")
    help_text = models.CharField(
        max_length=255,
        null=True, verbose_name="Additional help text to the question?")
    question_type = models.CharField(
        max_length=50,
        choices=QUESTION_TYPES, verbose_name="Type of the question")
    is_required = models.BooleanField(
        default=True, verbose_name="Is the answer to the question required?")
    choices = models.TextField(
        null=True, verbose_name="List all available options, comma separated",
        help_text="Used only with 'Choices' question type")
    is_multiple_choice = models.BooleanField(
        default=False, verbose_name="Are there multiple choices allowed?",
        help_text="Used only with 'Choices' question type")
    order = models.PositiveIntegerField(
        null=False, blank=False, help_text="Position of the question")

    class Meta:
        ordering = ('form', 'order')

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
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(
        max_length=50,
        choices=APPLICATION_STATES, verbose_name="State of the application",
        null=True
    )

    def __unicode__(self):
        return str(self.pk)


class Answer(models.Model):
    application = models.ForeignKey(Application, null=False, blank=False)
    question = models.ForeignKey(Question, null=False, blank=False)
    answer = models.TextField()
