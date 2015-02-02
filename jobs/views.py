from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy

from .models import Job, Company
from .forms import JobForm


def jobs(request):
    job_offers = Job.objects.filter(ready_to_publish=True).filter(expiration_date__gte=timezone.now())
    return render(
        request, 
        'jobs/jobs.html', 
        {
            'job_offers': job_offers
        }
    )

def job_details(request, id):
    queryset = Job.objects.filter(ready_to_publish=True).filter(expiration_date__gte=timezone.now())
    job = get_object_or_404(queryset, id=id)
    return TemplateResponse(
        request,
        'jobs/job_details.html',
        {
            'job': job,
        }
    )


class JobCreate(CreateView):
    model = Job
    template_name = 'jobs/job_edit.html'
    form_class = JobForm
    success_url = reverse_lazy('jobs:jobs')

    def form_valid(self, form):
        company, created = Company.objects.get_or_create(name=form.cleaned_data['company_name'])
        form.instance.company = company
        form.instance.created = timezone.now()
        return super(JobCreate, self).form_valid(form)