from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy

from .models import Job, Meetup
from .forms import JobForm, MeetupForm


def main(request):
    job_offers = Job.objects.filter(
        ready_to_publish=True,
        published_date__isnull=False,
        expiration_date__gte=timezone.now()
    ).order_by('-published_date')[:4]
    meetup_list = Meetup.objects.filter(
        ready_to_publish=True,
        published_date__isnull=False,
        expiration_date__gte=timezone.now()
    ).order_by('-published_date')[:3]
    return render(
        request,
        'jobs/main.html',
        {
            'meetup_list': meetup_list,
            'job_offers': job_offers
            }
    )


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

def confirm_submission(request):
    return TemplateResponse(
        request,
        'jobs/confirm_submission.html'
    )

class JobCreate(SuccessMessageMixin, CreateView):
    model = Job
    template_name = 'jobs/job_edit.html'
    form_class = JobForm
    success_url = reverse_lazy('jobs:confirm_submission')
    success_message = 'Your job offer was added to our database, \
                    you will receive further information shortly.'

    def form_valid(self, form):
        return super(JobCreate, self).form_valid(form)


class MeetupCreate(SuccessMessageMixin, CreateView):
    model = Meetup
    template_name = 'jobs/meetup_edit.html'
    form_class = MeetupForm
    success_url = reverse_lazy('jobs:confirm_submission')
    success_message = 'Your meetup was added to our database, \
                    you will receive further information shortly.'

    def form_valid(self, form):
        return super(MeetupCreate, self).form_valid(form)
