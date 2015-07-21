from datetimewidget.widgets import DateTimeWidget
from django import forms
from ckeditor.widgets import CKEditorWidget

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
        widget=DateTimeWidget(
            attrs={'id': "start_date_time"},
            usel10n=True,
            bootstrap_version=3
        )
    )
    meetup_end_date = forms.DateTimeField(
        widget=DateTimeWidget(
            attrs={'id': "end_date_time"},
            usel10n=True,
            bootstrap_version=3
        )
    )
    description = forms.CharField(widget=CKEditorWidget())
    website = forms.URLField(
        initial='http://',
        help_text='Rememeber to start with http:// or https://'
    )

    class Meta:
        model = Meetup
        fields = ['title', 'organisation', 'meetup_type', 'contact_email',
            'website', 'city', 'country', 'description', 'is_recurring',
            'recurrence', 'meetup_start_date', 'meetup_end_date'
        ]
