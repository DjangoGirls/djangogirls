from datetimewidget.widgets import DateTimeWidget
from django import forms
from ckeditor.widgets import CKEditorWidget

from jobs.models import Job, Meetup


class JobForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    website = forms.URLField(
        initial='http://',
        help_text='Rememebr to start with http:// or https://'
    )
    cities = forms.CharField(
        help_text="If you have opportunities in several \
            countries, please either specify that in the job description, \
            or add job opportunities for each country in which you have a space."
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
        help_text='Rememebr to start with http:// or https://'
    )

    class Meta:
        model = Meetup
        fields = ['title', 'organisation', 'meetup_type', 'contact_email',
            'website', 'city', 'country', 'description', 'is_recurring',
            'recurrence', 'meetup_start_date', 'meetup_end_date'
        ]
