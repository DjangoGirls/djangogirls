from django import forms

from core.models import Event
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

    def clean_has_organized_before(self):
        data = self.cleaned_data
        if (data.get('has_organized_before') == 'True' and
                not data.get('previous_event')):
            raise forms.ValidationError('You have to choose an event.')

        return data


class ApplicationForm(forms.Form):
    about_you = forms.CharField(widget=forms.Textarea)
    why = forms.CharField(widget=forms.Textarea)
    involvement = forms.MultipleChoiceField(
        choices=INVOLVEMENT_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple)
    experience = forms.CharField(widget=forms.Textarea)


class OrganizersForm(forms.Form):
    main_organizer_email = forms.EmailField()
    main_organizer_first_name = forms.CharField(max_length=30)
    main_organizer_last_name = forms.CharField(max_length=30)


class WorkshopForm(forms.Form):
    pass
