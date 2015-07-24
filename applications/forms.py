from django import forms
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError

from .models import Application, Answer, Question, Score, Email
from .utils import generate_form_from_questions


class ApplicationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        """
        The form here is programatically generated out of Question objects
        """

        questions = kwargs.pop('questions')
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields = generate_form_from_questions(questions)


    def save(self, *args, **kwargs):
        form = kwargs.pop('form')
        application = Application.objects.create(form=form)

        for name in self.cleaned_data:
            question = None
            pk = name.replace('question_', '')
            value = self.cleaned_data[name]
            try:
                question = Question.objects.get(pk=pk, form=form)
            except (Question.DoesNotExist, ValueError):
                if name == 'newsletter_optin':
                    if value == 'yes':
                        application.newsletter_optin = True
                    else:
                        application.newsletter_optin = False
                    application.save()

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
            subject = "Confirmation of your application for {}".format(form.page.title)
            body = render_to_string(
                'emails/application_confirmation.html',
                {
                    'application': application,
                    'intro': form.confirmation_mail,
                }
            )
            sender = "{} <{}>".format(form.page.title, form.page.event.email)
            msg = EmailMessage(subject, body, sender, [application.email,])
            msg.content_subtype = "html"
            try:
                msg.send()
            except:
                # TODO: what should we do when sending fails?
                pass


class ScoreForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = ['score', 'comment']

    def clean(self):
        cleaned_data = super(ScoreForm, self).clean()
        score = cleaned_data.get('score')
        comment = cleaned_data.get('comment')
        if not score and not comment:
            raise forms.ValidationError('You must enter a score or a comment to'+ 
                'save this application.')


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
        model = Email
        fields = ['recipients_group', 'subject', 'text']
