from django import forms

from ckeditor.widgets import CKEditorWidget
from bootstrap3_datetime.widgets import DateTimePicker

from jobs.models import Job, Meetup


class JobForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    website = forms.URLField(
        initial='http://',
        help_text='Rememeber to start with http:// or https://'
    )
    cities = forms.CharField(
        help_text="List the cities where this opportunity is available. \
            If you have opportunities in cities in more than one country, \
            please submit a separate job opportunity per country."
    )
    expiration_date = forms.DateField(
        required=False,
        help_text="Enter the date until which the post should be published. "
                  "By default, it is set to 60 days from posting.",
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))

    class Meta:
        model = Job
        fields = ('company', 'website', 'contact_email', 'title',
                  'description', 'cities', 'country', 'remote_work', 'relocation')
        # custom labels
        labels = {
            'title': 'Job title'
        }



class MeetupForm(forms.ModelForm):
    meetup_start_date = forms.DateTimeField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": False}))
    meetup_end_date = forms.DateTimeField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": False}))
    description = forms.CharField(widget=CKEditorWidget())
    website = forms.URLField(
        initial='http://',
        help_text='Rememeber to start with http:// or https://'
    )
    expiration_date = forms.DateField(
        required=False,
        help_text="Enter the date until which the post should be published. "
                  "By default, it is set to 60 days from posting.",
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))

    class Meta:
        model = Meetup
        fields = ['title', 'organisation', 'meetup_type', 'contact_email',
            'website', 'city', 'country', 'description', 'is_recurring',
            'recurrence', 'meetup_start_date', 'meetup_end_date', 'expiration_date'
        ]
