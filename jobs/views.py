from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.contrib import messages

from django.template.loader import get_template
from django.template import Context

from jobs.models import Job, Meetup
from jobs.forms import JobForm, MeetupForm
from jobs.community_mails import send_job_mail, send_meetup_mail


def main(request):
    job_offers = Job.visible_objects.all().order_by('-published_date')[:4]
    meetup_list = Meetup.visible_objects.all().order_by('-published_date')[:3]
    return render(
        request,
        'jobs/main.html',
        {
            'meetup_list': meetup_list,
            'job_offers': job_offers
            }
    )


def jobs(request):
    job_offers = Job.visible_objects.all()
    return render(
        request,
        'jobs/jobs.html',
        {
            'job_offers': job_offers,
        }
    )


def meetups(request):
    meetup_list = Meetup.visible_objects.all()
    return TemplateResponse(
        request,
        'jobs/meetups.html',
        {
            'meetup_list': meetup_list,
        }
    )


def job_details(request, id):
    queryset = Job.visible_objects.all()
    job = get_object_or_404(queryset, id=id)
    return TemplateResponse(
        request,
        'jobs/job_details.html',
        {
            'job': job,
        }
    )


def meetup_details(request, id):
    queryset = Meetup.visible_objects.all()
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


def create_job(request):
    job_form = JobForm()
    success_message = 'Your job offer was added to our database, \
                    you will receive further information shortly.'
    if request.method == 'POST':
        job_form = JobForm(request.POST)
        if job_form.is_valid():
            new_job = job_form.save()
            messages.add_message(
                request,
                messages.INFO,
                success_message
            )
            subject = '{0} was submitted succesfully.'.format(new_job.title)
            context = Context({'option': new_job.title})
            message_plain = get_template(
            'jobs/email_templates/community_confirm.txt').render(context)
            message_html = get_template(
                'jobs/email_templates/community_confirm.html').render(context)
            recipient = new_job.contact_email
            send_job_mail(
                subject,
                message_plain,
                message_html,
                recipient
            )
            return redirect('jobs:confirm_submission')
    return TemplateResponse(
        request,
        'jobs/job_edit.html',
        {
            'form': job_form,
        }
    )


def create_meetup(request):
    meetup_form = MeetupForm()
    success_message = 'Your meetup was added to our database, \
                    you will receive further information shortly.'
    if request.method == 'POST':
        meetup_form = MeetupForm(request.POST)
        if meetup_form.is_valid():
            new_meetup = meetup_form.save()
            messages.add_message(
                request,
                messages.INFO,
                success_message
            )
            subject = '{0} was submitted succesfully.'.format(new_meetup.title)
            context = Context({'option': new_meetup.title})
            message_plain = get_template(
            'jobs/email_templates/community_confirm.txt').render(context)
            message_html = get_template(
                'jobs/email_templates/community_confirm.html').render(context)
            recipient = new_meetup.contact_email
            send_meetup_mail(
                subject,
                message_plain,
                message_html,
                recipient
            )
            return redirect('jobs:confirm_submission')
    return TemplateResponse(
        request,
        'jobs/meetup_edit.html',
        {
            'form': meetup_form,
        }
    )
