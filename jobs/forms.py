from datetimewidget.widgets import DateTimeWidget
from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Job, Meetup


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

    def clean(self):
        super(JobForm, self).clean()
        if 'save' in self.data:
            try:
                company = Company.objects.get(
                    name=self.cleaned_data['company_name'],
                )
                if company.website != self.cleaned_data['website']:
                    self.show_overwrite = True
                    raise forms.ValidationError(
                        "The company %(name)s already exists with the "
                        "following website: %(www)s. Do you want to overwrite "
                        "this website?",
                        params={'name': company.name, 'www': company.website},
                        )
            except (Company.DoesNotExist, KeyError):
                pass
        return self.cleaned_data

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
