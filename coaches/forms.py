from django import forms
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .models import CoachApplication, Answer, Question, CoachEmail
from .utils import generate_form_from_coach_questions


class CoachApplicationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        """
        The form here is programmattically generated out of Question objects
        """

        questions = kwargs.pop('questions')
        super(CoachApplicationForm, self).__init__(*args, **kwargs)
        self.fields = generate_form_from_coach_questions(questions)

    def save(self, *args, **kwargs):
        form = kwargs.pop('form')
        application = CoachApplication.objects.create(form=form)

        for name in self.cleaned_data:
            question = None
            pk = name.replace('question_', '')
            value = self.cleaned_data[name]
            try:
                question = Question.objects.get(pk=pk, form=form)
            except (Question.DoesNotExist, ValueError):
                pass

            value = ', '.join(value) if type(value) == list else value

            if question:
                Answer.objects.create(
                    application=application,
                    question=question,
                    answer=value
                )

                if question.question_type == 'email':
                    application.email = value
                    application.save()

        if not form.page.event.email:
            # If event doesn't have an email (legacy events), create
            # it just by taking the url. In 99% cases, it is correct.
            form.page.event.email = "{}@djangogirls.org".format(form.page.url)
            form.page.event.save()

        if application.email:
            # Send confirmation email
            subject = "Confirmation of your coach registration for {}".format(form.page.title)
            body = render_to_string(
                'emails/coach_application_confirmation.html',
                {
                    'application': application,
                    'intro': form.confirmation_mail,
                }
            )
            msg = EmailMessage(subject, body, form.page.event.email, [application.email, ])
            msg.content_subtype = "html"
            try:
                msg.send()
            except:
                # TODO: what should we do when sending fails?
                pass


class EmailForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        When email is already sent, the form should be disabled
        """
        super(EmailForm, self).__init__(*args, **kwargs)
        if self.instance.sent:
            # email was sent, let's disable all fields:
            for field in self.fields:
                self.fields[field].widget.attrs['disabled'] = True

    class Meta:
        model = CoachEmail
        fields = ['recipients_group', 'subject', 'text']
