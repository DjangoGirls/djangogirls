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
        required=False)

    def clean(self):
        data = self.cleaned_data
        if (data.get('has_organized_before') is True and
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


class WorkshopForm(forms.Form):
    pass


class OrganizersForm(forms.Form):
    pass
