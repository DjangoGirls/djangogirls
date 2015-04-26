from django.db import models
from django.core.mail import send_mail
from django.contrib import admin, messages
from django.template.loader import get_template
from django.template import Context
from django.conf.urls import patterns, url
from django.shortcuts import redirect, get_object_or_404

from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget, AutosizedTextarea

from djangogirls.local_settings import JOBS_EMAIL_USER, JOBS_EMAIL_PASSWORD
from djangogirls.local_settings import MEETUPS_EMAIL_PASSWORD, MEETUPS_EMAIL_USER
from .models import PublishFlowModel, Job, Meetup


def make_published(modeladmin, request, queryset):
    for item in queryset:
        if item.review_status == PublishFlowModel.READY_TO_PUBLISH:
            item.publish()
make_published.short_description = "Publish selected items"


def send_status_update_job_offer(modeladmin, request, queryset):
    for item in queryset:
        subject = "Status update on your job offer - {0}.".format(item.title)
        message_plain = get_template(
            'jobs/email_templates/job_status.txt').render(
                Context({'status': item.get_review_status_display()})
        )
        message_html = get_template(
            'jobs/email_templates/job_status.html').render(
                Context({'status': item.get_review_status_display()})
        )
        send_from = "jobs@djangogirls.org"
        recipient = [item.contact_email, ]
        send_mail(
            subject,
            message_plain,
            send_from,
            recipient,
            auth_user=JOBS_EMAIL_USER,
            auth_password=JOBS_EMAIL_PASSWORD,
            html_message=message_html,
        )
        if send_mail != 0:
            messages.add_message(
                request,
                messages.INFO,
                'Email to {0} has been sent.'.format(' '.join(recipient))
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'Email to {0} has NOT been sent.'.format(' '.join(recipient))
            )
send_status_update_job_offer.short_description = "Send notification about job offer status."


def send_status_update_meetup(modeladmin, request, queryset):
    for item in queryset:
        subject = "Status update on your meetup - {0}.".format(item.title)
        message_plain = get_template(
            'jobs/email_templates/meetup_status.txt').render(
                Context({'status': item.get_review_status_display()})
        )
        message_html = message_plain = get_template(
            'jobs/email_templates/meetup_status.html').render(
                Context({'status': item.get_review_status_display()})
        )
        send_from = "meetups@djangogirls.org"
        recipient = [item.contact_email, ]
        send_mail(
            subject,
            message_plain,
            send_from,
            recipient,
            auth_user=MEETUPS_EMAIL_USER,
            auth_password=MEETUPS_EMAIL_PASSWORD,
            html_message=message_html
        )
        if send_mail != 0:
            messages.add_message(
                request,
                messages.INFO,
                'Email to {0} has been sent.'.format(' '.join(recipient))
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'Email to {0} has NOT been sent.'.format(' '.join(recipient))
            )
send_status_update_meetup.short_description = "Send notification about meetup status."


class JobAdmin(admin.ModelAdmin):
    readonly_fields = ('reviewer', 'published_date')
    list_display = ['title', 'company', 'reviewer', 'review_status']
    ordering = ['title']
    actions = [make_published, send_status_update_job_offer]
    formfield_overrides = {
        models.DateField: {'widget': SuitDateWidget},
        models.TextField: {'widget': AutosizedTextarea},
    }

    def get_urls(self):
        urls = super(JobAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'^(?P<id>\d+)/assign/$',
                self.assign_job_reviewer,
                name='assign_job_reviewer'
            ),
            url(
                r'^(?P<id>\d+)/unassign/$',
                self.unassign_job_reviewer,
                name='unassign_job_reviewer'
            ),
        )
        return my_urls + urls

    def assign_job_reviewer(self, request, id):
        job = get_object_or_404(Job, id=id)
        job.reviewer = request.user
        job.save()
        return redirect('/admin/jobs/job/%s/' % id)

    def unassign_job_reviewer(self, request, id):
        job = get_object_or_404(Job, id=id)
        job.reviewer = None
        job.save()
        return redirect('/admin/jobs/job/%s/' % id)


class MeetupAdmin(admin.ModelAdmin):
    readonly_fields = ('reviewer', 'published_date',)
    list_display = ['title', 'city', 'reviewer', 'review_status']
    ordering = ['title']
    actions = [make_published, send_status_update_meetup]
    formfield_overrides = {
        models.DateField: {'widget': SuitDateWidget},
        models.DateTimeField: {'widget': SuitSplitDateTimeWidget},
        models.TextField: {'widget': AutosizedTextarea},
    }

    def get_urls(self):
        urls = super(MeetupAdmin, self).get_urls()
        my_urls = patterns('',
            url(
                r'^(?P<id>\d+)/assign/$',
                self.assign_meetup_reviewer,
                name='assign_meetup_reviewer'
            ),
            url(
                r'^(?P<id>\d+)/unassign/$',
                self.unassign_meetup_reviewer,
                name='unassign_meetup_reviewer'
            ),
        )
        return my_urls + urls

    def assign_meetup_reviewer(self, request, id):
        meetup = get_object_or_404(Meetup, id=id)
        meetup.reviewer = request.user
        meetup.save()
        return redirect('/admin/jobs/meetup/%s/' % id)

    def unassign_meetup_reviewer(self, request, id):
        meetup = get_object_or_404(Meetup, id=id)
        meetup.reviewer = None
        meetup.save()
        return redirect('/admin/jobs/meetup/%s/' % id)


admin.site.register(Job, JobAdmin)
admin.site.register(Meetup, MeetupAdmin)
