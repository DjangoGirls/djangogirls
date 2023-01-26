from django import forms
from django.utils.translation import gettext_lazy as _
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField
from django_date_extensions.fields import ApproximateDateFormField

from core.models import Event
from core.validators import (
    validate_approximatedate,
    validate_event_date,
    validate_future_date,
    validate_local_restrictions,
)

from .constants import INVOLVEMENT_CHOICES

PREVIOUS_ORGANIZER_CHOICES = (
    (True, _("Yes, I organized Django Girls")),
    (False, _("No, it’s my first time organizing Django Girls")),
)

WORKSHOP_CHOICES = ((True, _("Remote")), (False, _("In-Person")))


class PreviousEventForm(forms.Form):
    has_organized_before = forms.TypedChoiceField(
        coerce=lambda x: x in ["True", True],
        widget=forms.RadioSelect,
        choices=PREVIOUS_ORGANIZER_CHOICES,
        required=True,
    )
    previous_event = forms.ModelChoiceField(
        queryset=Event.objects.past(),
        empty_label=_("Choose event"),
        required=False,
        widget=forms.Select(attrs={"aria-label": _("Choose event"), "class": "linked-select"}),
    )

    def clean(self):
        has_organized_before = self.cleaned_data.get("has_organized_before")
        previous_event = self.cleaned_data.get("previous_event")
        if has_organized_before is True and not previous_event:
            self.add_error("has_organized_before", _("You have to choose an event."))

        return self.cleaned_data

    def get_data_for_saving(self):
        data = self.cleaned_data
        # Clean the previous event if someone filled it
        # and marked themselves as first-time organizers
        if not data["has_organized_before"]:
            data["previous_event"] = None
        del data["has_organized_before"]
        return data


class ApplicationForm(forms.Form):
    about_you = forms.CharField(widget=forms.Textarea(attrs={"class": "compact-input"}))
    why = forms.CharField(widget=forms.Textarea(attrs={"class": "compact-input"}))
    involvement = forms.MultipleChoiceField(choices=INVOLVEMENT_CHOICES, widget=forms.CheckboxSelectMultiple)
    experience = forms.CharField(widget=forms.Textarea(attrs={"class": "compact-input"}))

    def get_data_for_saving(self):
        data = self.cleaned_data
        data["involvement"] = ", ".join(data.get("involvement"))
        return data


class BaseOrganizerFormSet(forms.BaseFormSet):
    def get_data_for_saving(self):
        organizers = [form.cleaned_data for form in self.forms if form.has_changed()]
        main_organizer = organizers.pop(0)
        data = {
            "main_organizer_email": main_organizer["email"],
            "main_organizer_first_name": main_organizer["first_name"],
            "main_organizer_last_name": main_organizer["last_name"],
            "coorganizers": organizers,
        }
        return data


class OrganizerForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "compact-input"}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "compact-input"}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"class": "compact-input"}))


OrganizersFormSet = forms.formset_factory(
    OrganizerForm, formset=BaseOrganizerFormSet, extra=1, max_num=10, min_num=1, validate_min=True
)


class WorkshopForm(forms.Form):
    date = ApproximateDateFormField(widget=forms.TextInput(attrs={"class": "compact-input"}))
    city = forms.CharField(required=True, max_length=200, widget=forms.TextInput(attrs={"class": "compact-input"}))
    country = LazyTypedChoiceField(choices=[(None, "Choose country")] + list(countries))
    venue = forms.CharField(widget=forms.Textarea(attrs={"class": "compact-input"}))
    sponsorship = forms.CharField(widget=forms.Textarea(attrs={"class": "compact-input"}))
    coaches = forms.CharField(widget=forms.Textarea(attrs={"class": "compact-input"}))
    local_restrictions = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "compact-input"}))
    safety = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "compact-input"}))
    diversity = forms.CharField(widget=forms.Textarea(attrs={"class": "compact-input"}))
    additional = forms.CharField(widget=forms.Textarea(attrs={"class": "compact-input"}))
    confirm_covid_19_protocols = forms.BooleanField()

    def clean_date(self):
        date = self.cleaned_data.get("date")
        validate_approximatedate(date)
        # Check if the event is in the future
        validate_future_date(date)
        # Check if date is 3 months away
        validate_event_date(date)
        return date

    def get_data_for_saving(self):
        return self.cleaned_data

    def clean_local_restrictions(self):
        local_restrictions = self.cleaned_data.get("local_restrictions")
        # Check if organizer provides link to government website
        validate_local_restrictions(local_restrictions)
        return local_restrictions


class RemoteWorkshopForm(forms.Form):
    date = ApproximateDateFormField(widget=forms.TextInput(attrs={"class": "compact-input"}))
    city = forms.CharField(required=True, max_length=200, widget=forms.TextInput(attrs={"class": "compact-input"}))
    country = LazyTypedChoiceField(choices=[(None, _("Choose country"))] + list(countries))
    sponsorship = forms.CharField(widget=forms.Textarea(attrs={"class": "compact-input"}))
    coaches = forms.CharField(widget=forms.Textarea(attrs={"class": "compact-input"}))
    tools = forms.CharField(widget=forms.Textarea(attrs={"class": "compact-input"}))
    diversity = forms.CharField(widget=forms.Textarea(attrs={"class": "compact-input"}))
    additional = forms.CharField(widget=forms.Textarea(attrs={"class": "compact-input"}))

    def clean_date(self):
        date = self.cleaned_data.get("date")
        validate_approximatedate(date)
        # Check if the event is in the future
        validate_future_date(date)
        # Check if date is 3 months away
        validate_event_date(date)
        return date

    def get_data_for_saving(self):
        return self.cleaned_data


class WorkshopTypeForm(forms.Form):
    remote = forms.TypedChoiceField(
        coerce=lambda x: x in ["True", True], widget=forms.RadioSelect, choices=WORKSHOP_CHOICES, required=True
    )

    def get_data_for_saving(self):
        return self.cleaned_data
