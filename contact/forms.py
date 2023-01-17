from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_bleach.forms import BleachField

from contact.models import ContactEmail
from core.forms import BetterReCaptchaField, EventChoiceField
from core.models import Event


class ContactForm(forms.ModelForm):
    event = EventChoiceField(
        queryset=Event.objects.public().distinct("city", "country").order_by("city"),
        required=False,
        label=_("Django Girls workshop in..."),
    )
    captcha = BetterReCaptchaField()
    message = BleachField()

    class Meta:
        model = ContactEmail
        fields = (
            "name",
            "email",
            "contact_type",
            "event",
            "message",
        )
        widgets = {"contact_type": forms.RadioSelect}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if settings.RECAPTCHA_TESTING:
            del self.fields["captcha"]

    def clean_event(self):
        contact_type = self.cleaned_data.get("contact_type")
        event = self.cleaned_data.get("event")
        if contact_type == ContactEmail.CHAPTER:
            if not event:
                raise forms.ValidationError(_("Please select the event"))
        return event
