from django import forms
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField
from django_date_extensions.fields import ApproximateDateFormField

from core.models import Event
from core.validators import validate_approximatedate
from .constants import INVOLVEMENT_CHOICES

PREVIOUS_ORGANIZER_CHOICES = (
    (True, "Yes, I organized Django Girls"),
    (False, "No, it’s my first time organizing Django Girls"))


class PreviousEventForm(forms.Form):
    has_organized_before = forms.TypedChoiceField(
        coerce=lambda x: x in ['True', True],
        widget=forms.RadioSelect,
        choices=PREVIOUS_ORGANIZER_CHOICES,
        required=True)
    previous_event = forms.ModelChoiceField(
        queryset=Event.objects.past(),
        empty_label="Choose event",
        required=False,
        widget=forms.Select(
            attrs={'aria-label': 'Choose event', 'class': 'linked-select'}))

    def clean(self):
        has_organized_before = self.cleaned_data.get('has_organized_before')
        previous_event = self.cleaned_data.get('previous_event')
        if has_organized_before is True and not previous_event:
            self.add_error(
                'has_organized_before',
                'You have to choose an event.')

        return self.cleaned_data

    def get_data(self):
        data = self.cleaned_data
        del data['has_organized_before']
        return data


class ApplicationForm(forms.Form):
    about_you = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'compact-input'}))
    why = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'compact-input'}))
    involvement = forms.MultipleChoiceField(
        choices=INVOLVEMENT_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple)
    experience = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'compact-input'}))

    def get_data(self):
        data = self.cleaned_data
        data["involvement"] = ", ".data.get('involvement')
        return data


class BaseOrganizerFormSet(forms.BaseFormSet):
    def get_data(self):
        organizers = [form.cleaned_data
                      for form in self.forms if form.has_changed()]
        main_organizer = organizers.pop(0)
        data = {
            'main_organizer_email': main_organizer['email'],
            'main_organizer_first_name': main_organizer['first_name'],
            'main_organizer_last_name': main_organizer['last_name'],
            'coorganizers': organizers
        }
        return data


class OrganizerForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'compact-input'}))
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'compact-input'}))
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'compact-input'}))


OrganizersFormSet = forms.formset_factory(
    OrganizerForm, formset=BaseOrganizerFormSet, extra=1, max_num=10,
    min_num=1, validate_min=True)


class WorkshopForm(forms.Form):
    date = ApproximateDateFormField(
        widget=forms.TextInput(attrs={'class': 'compact-input'}))
    city = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'compact-input'}))
    country = LazyTypedChoiceField(choices=countries)
    website_slug = forms.SlugField(
        widget=forms.TextInput(attrs={'class': 'compact-input'}))
    venue = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'compact-input'}))
    sponsorship = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'compact-input'}))
    coaches = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'compact-input'}))

    def clean_date(self):
        date = self.cleaned_data.get('date')
        validate_approximatedate(date)
        # TODO: add checking if the event is in the future
        return date

    def get_data(self):
        return self.cleaned_data
