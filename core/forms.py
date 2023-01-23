from captcha.fields import ReCaptchaField
from django import forms
from django.conf import settings
from django.core.validators import validate_email
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from .models import Event


class BetterReCaptchaField(ReCaptchaField):
    """A ReCaptchaField that always works in DEBUG mode"""

    def clean(self, values):
        if settings.DEBUG:
            return values[0]
        return super().clean(values)


class AddOrganizerForm(forms.Form):
    """
    Custom form for adding new organizers to an existing event.

    If user of given email already exists, they're added to the event and
    receive e-mail notification about it.

    If user is new, they're created (randomly generated password), invited
    to Slack and receive e-mail notification with instructions to login
    (including password).
    """

    event = forms.ModelChoiceField(queryset=Event.objects.all())
    name = forms.CharField(label=_("Organizer's first and last name"))
    email = forms.CharField(label=_("E-mail address"), validators=[validate_email])

    def __init__(self, *args, **kwargs):
        event_choices = kwargs.pop("event_choices", None)
        super().__init__(*args, **kwargs)
        if event_choices is not None:
            self.fields["event"].queryset = event_choices

    def save(self, *args, **kwargs):
        assert self.is_valid()
        self._errors = []
        email = self.cleaned_data["email"]
        event = self.cleaned_data["event"]
        first_name, _, last_name = self.cleaned_data["name"].partition(" ")
        user = event.add_organizer(email, first_name, last_name)
        return user


class EventChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.city}, {obj.country}"


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["city", "country", "date", "email", "latlng", "name", "page_title", "page_url"]

    @transaction.atomic
    def save(self, commit=True):
        """Save the event and create default content in case of new instances"""
        created = not self.instance.pk
        instance = super().save(commit=commit)
        if commit and created:
            # create default content
            instance.add_default_content()
            instance.add_default_menu()

        return instance
