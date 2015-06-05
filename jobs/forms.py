from datetimewidget.widgets import DateTimeWidget
from django import forms
from ckeditor.widgets import CKEditorWidget

from jobs.models import Job, Meetup


class JobForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Job
        fields = ('company', 'website', 'contact_email', 'title',
                  'description', 'cities', 'country')
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

    class Meta:
        model = Meetup
        fields = ['title', 'organisation', 'meetup_type', 'contact_email',
            'website', 'city', 'country', 'description', 'is_recurring',
            'recurrence', 'meetup_start_date', 'meetup_end_date'
        ]
