from django.utils import timezone

from django.shortcuts import render, get_object_or_404, render_to_response
from django.template.response import TemplateResponse
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy

from .models import Job, Meetup, Company
from .forms import JobForm


def jobs(request):
    job_offers = Job.objects.filter(
        ready_to_publish=True,
        published_date__isnull=False,
        expiration_date__gte=timezone.now()
    )
    return render(
        request,
        'jobs/jobs.html',
        {
            'job_offers': job_offers,
        }
    )


def meetups(request):
    meetup_list = Meetup.objects.filter(
        ready_to_publish=True,
        published_date__isnull=False,
        expiration_date__gte=timezone.now()
    )
    return TemplateResponse(
        request,
        'jobs/meetups.html',
        {
            'meetup_list': meetup_list,
        }
    )


def job_details(request, id):
    queryset = Job.objects.filter(
        ready_to_publish=True,
        published_date__isnull=False,
        expiration_date__gte=timezone.now()
    )
    job = get_object_or_404(queryset, id=id)
    return TemplateResponse(
        request,
        'jobs/job_details.html',
        {
            'job': job,
        }
    )


def meetup_details(request, id):
    queryset = Meetup.objects.filter(
        ready_to_publish=True,
        published_date__isnull=False,
        expiration_date__gte=timezone.now()
    )
    meetup = get_object_or_404(queryset, id=id)
    return TemplateResponse(
        request,
        'jobs/meetup_details.html',
        {
            'meetup': meetup,
        }
    )


class JobCreate(CreateView):
    model = Job
    template_name = 'jobs/job_edit.html'
    form_class = JobForm
    success_url = reverse_lazy('jobs:jobs')

    def form_valid(self, form):
        job = form.save(commit=False)
        if 'save' in form.data:
            company, created = Company.objects.get_or_create(
                name=form.cleaned_data['company_name'],
                website=form.cleaned_data['website']
            )
            job.company = company
        elif 'overwrite' in form.data:
            company = Company.objects.get(name=form.cleaned_data['company_name'])
            company.website = form.cleaned_data['website']
            company.save()
            job.company = company
        elif 'keep' in form.data:
            company = Company.objects.get(name=form.cleaned_data['company_name'])
            job.company = company
        job.save()
        return super(JobCreate, self).form_valid(form)
