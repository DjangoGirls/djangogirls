import hashlib

import requests
from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from core.forms import BetterReCaptchaField

from .models import Answer, Application, Email, Question, Score
from .questions import generate_form_from_questions


class ApplicationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        """
        The form here is programatically generated out of Question objects
        """
        self.form = kwargs.pop("form")
        self.base_fields = generate_form_from_questions(self.form.question_set.all())
        if not settings.RECAPTCHA_TESTING:
            self.base_fields.update({"captcha": BetterReCaptchaField()})
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        question = Question.objects.filter(form=self.form, question_type="email").first()

        if not question:
            return cleaned_data

        field_name = f"question_{question.pk}"
        email = self.cleaned_data.get(field_name)

        if email is not None:
            existing_application = Application.objects.filter(form=self.form, email=email)
            if existing_application.exists():
                self.add_error(field_name, _("Application for this e-mail already exists."))

        # Always return cleaned_data
        return cleaned_data

    def save(self, *args, **kwargs):
        application = Application(form=self.form)
        answers = []

        for name in self.cleaned_data:
            question = None
            pk = name.replace("question_", "")
            value = self.cleaned_data[name]
            try:
                question = Question.objects.get(pk=pk, form=self.form)
            except (Question.DoesNotExist, ValueError):
                if name == "newsletter_optin":
                    if value == "yes":
                        application.newsletter_optin = True
                    else:
                        application.newsletter_optin = False

            value = ", ".join(value) if type(value) == list else value

            if question:
                answers.append(Answer(question=question, answer=value))

                if question.question_type == "email":
                    application.email = value

        if not self.form.event.email:
            # If event doesn't have an email (legacy events), create
            # it just by taking the url. In 99% cases, it is correct.
            self.form.event.email = f"{self.form.event.page_url}@djangogirls.org"
            self.form.event.save()

        if application.email:
            # Send confirmation email
            subject = _("Confirmation of your application for %(page_title)s") % {
                "page_title": self.form.event.page_title
            }
            body = render_to_string(
                "emails/application_confirmation.html",
                {
                    "application": application,
                    "intro": self.form.confirmation_mail,
                },
            )
            msg = EmailMessage(
                subject,
                body,
                self.form.event.email,
                [
                    application.email,
                ],
            )
            msg.content_subtype = "html"
            try:
                msg.send()
            except:
                # TODO: what should we do when sending fails?
                pass

        # Adding applicant email to Django Girls Dispatch
        if application.newsletter_optin and application.email:
            emailb = application.email.encode()
            emailhash = hashlib.md5(emailb).hexdigest()
            r = requests.get(
                "https://us8.api.mailchimp.com/3.0/lists/d278270e6f/members/%s" % emailhash,
                auth=("user", settings.MAILCHIMP_API_KEY),
            )
            # Mailchimp will return a 404 if the email we want to add is not on
            # the Dispatch subscriber list
            if r.status_code == 404:
                url = "https://us8.api.mailchimp.com/3.0/lists/d278270e6f/members/"
                payload = {"email_address": application.email, "status": "pending"}
                requests.post(url, auth=("user", settings.MAILCHIMP_API_KEY), json=payload)

        with transaction.atomic():
            application.save()
            for answer in answers:
                answer.application = application
            Answer.objects.bulk_create(answers)


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ["score", "comment"]


class EmailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        When email is already sent, the form should be disabled
        """
        super().__init__(*args, **kwargs)
        if self.instance.sent:
            # email was sent, let's disable all fields:
            for field in self.fields:
                self.fields[field].widget.attrs["disabled"] = True

    class Meta:
        model = Email
        fields = ["recipients_group", "subject", "text"]
