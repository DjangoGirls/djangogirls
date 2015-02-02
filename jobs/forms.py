from django import forms

from .models import Job


class JobForm(forms.ModelForm):

    company_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = Job
        fields = ('contact_email', 'title', 'description', 'city',
                  'country', 'expiration_date')
        exclude = ('company',)
