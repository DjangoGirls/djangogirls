from django import forms

from .models import Job, Company


class JobForm(forms.ModelForm):

    show_overwrite = False
    company_name = forms.CharField(label='Company',
                                   max_length=500,
                                   required=True)
    website = forms.URLField(label='Company website', required=True)

    class Meta:
        model = Job
        fields = ('company_name', 'website', 'contact_email', 'title',
                  'description', 'city', 'country')
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
