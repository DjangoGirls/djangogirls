from django import forms
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField
from django_date_extensions.fields import ApproximateDateFormField


from core.models import Event
from core.validators import validate_approximatedate
from .models import INVOLVEMENT_CHOICES

PREVIOUS_ORGANIZER_CHOICES = (
    (True, "Yes, I organized Django Girls"),
    (False, "No, it’s my first time organizing Django Girls"))


class PreviousEventForm(forms.Form):
    has_organized_before = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=PREVIOUS_ORGANIZER_CHOICES)
    previous_event = forms.ModelChoiceField(
        queryset=Event.objects.past(), empty_label="Choose event",
        required=False,
        widget=forms.Select(
            attrs={'aria-label': 'Choose event', 'class': 'linked-select'}))

    def clean(self):
        has_organized_before = self.cleaned_data.get('has_organized_before')
        previous_event = self.cleaned_data.get('previous_event')
        if (has_organized_before == 'True' and not previous_event):
            raise forms.ValidationError({
                'has_organized_before': ['You have to choose an event.']})

        return self.cleaned_data


class ApplicationForm(forms.Form):
    about_you = forms.CharField(widget=forms.Textarea(attrs={'class': 'compact-input'}))
    why = forms.CharField(widget=forms.Textarea(attrs={'class': 'compact-input'}))
    involvement = forms.MultipleChoiceField(
        choices=INVOLVEMENT_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple)
    experience = forms.CharField(widget=forms.Textarea(attrs={'class': 'compact-input'}))


class OrganizersForm(forms.Form):
    main_organizer_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'compact-input'}))
    main_organizer_first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'compact-input'}))
    main_organizer_last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'compact-input'}))


class WorkshopForm(forms.Form):
    date = ApproximateDateFormField(widget=forms.TextInput(attrs={'class': 'compact-input'}))
    city = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'compact-input'}))
    country = LazyTypedChoiceField(choices=countries)
    website_slug = forms.SlugField(widget=forms.TextInput(attrs={'class': 'compact-input'}))

    def clean_date(self):
        date = self.cleaned_data.get('date')
        validate_approximatedate(date)
        return self.clean_date
