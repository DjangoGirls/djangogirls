from django.db import models
from django.contrib import admin, messages
from django.template.loader import get_template
from django.template import Context
from django.conf.urls import patterns, url
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseBadRequest

from suit.widgets import (
    SuitDateWidget, SuitSplitDateTimeWidget, AutosizedTextarea)

from jobs.models import PublishFlowModel, Job, Meetup
from jobs.community_mails import send_job_mail


def make_published(modeladmin, request, queryset):
    for item in queryset:
        if item.review_status == PublishFlowModel.READY_TO_PUBLISH:
            item.publish()
        else:
            messages.add_message(
                request,
                messages.ERROR,
                "{0} couldn't be published.".format(item.title)
            )
make_published.short_description = "Publish selected items"


def send_status_update(modeladmin, request, queryset):
    for item in queryset:
        subject = "Status update on: {0}.".format(item.title)
        context = Context({
            'status': item.get_review_status_display(),
            'option': modeladmin.get_print_name(),
            'message_to_organisation': item.message_to_organisation,
        })
        message_plain = get_template(
            'jobs/email_templates/status.txt').render(context)
        message_html = get_template(
            'jobs/email_templates/status.html').render(context)
        recipient = item.contact_email
        status = send_job_mail(
            subject,
            message_plain,
            message_html,
            recipient,
        )
        messages.add_message(
            request,
            messages.INFO,
            status
        )
send_status_update.short_description = "Send notification about status."


class PublishFlowModelAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super(PublishFlowModelAdmin, self).get_urls()
        my_urls = [
            url(
                r'^(?P<id>\d+)/assign/$',
                self.admin_site.admin_view(self.assign_reviewer),
                name='assign_%s_reviewer' % self.get_print_name()
            ),
            url(
                r'^(?P<id>\d+)/unassign/$',
                self.admin_site.admin_view(self.unassign_reviewer),
                name='unassign_%s_reviewer' % self.get_print_name()
            ),
            url(
                r'^(?P<id>\d+)/accept/$',
                self.admin_site.admin_view(self.accept),
                name='accept_%s' % self.get_print_name()
            ),
            url(
                r'^(?P<id>\d+)/reject/$',
                self.admin_site.admin_view(self.reject),
                name='reject_%s' % self.get_print_name()
            ),
            url(
                r'^(?P<id>\d+)/restore/$',
                self.admin_site.admin_view(self.restore),
                name='restore_%s' % self.get_print_name()
            ),
            url(
                r'^(?P<id>\d+)/publish/$',
                self.admin_site.admin_view(self.publish),
                name='publish_%s' % self.get_print_name()
            ),
        ]
        return my_urls + urls

    def get_actions(self, request):
        actions = super(PublishFlowModelAdmin, self).get_actions(request)
        if request.user.groups.filter(name='Reviewers').exists():
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def get_print_name(self):
        return self.model._meta.model_name

    def not_expired(self, obj):
        return obj.not_expired
    not_expired.boolean = True
    not_expired.admin_order_field = 'not_expired'

    def assign_reviewer(self, request, id):
        try:
            post = get_object_or_404(self.model, id=id)
            post.assign(request.user)
            messages.add_message(
                request,
                messages.INFO,
                '{0} is now assigned.'.format(post.title)
            )
            return redirect('/admin/jobs/%s/%s/' % (self.get_print_name(), id))
        except AssertionError:
            return HttpResponseBadRequest(
                "It's not possible to assign reviewer: post is in a wrong state."
            )

    def unassign_reviewer(self, request, id):
        try:
            post = get_object_or_404(self.model, id=id)
            post.unassign()
            messages.add_message(
                request,
                messages.INFO,
                '{0} is now unassigned.'.format(post.title)
            )
            return redirect('/admin/jobs/%s/%s/' % (self.get_print_name(), id))
        except AssertionError:
            return HttpResponseBadRequest(
                "It's not possible to unassign reviewer: post is in a wrong state."
            )

    def accept(self, request, id):
        try:
            post = get_object_or_404(self.model, id=id)
            post.accept()
            messages.add_message(
                request,
                messages.INFO,
                '{0} is now accepted.'.format(post.title)
            )
            return redirect('/admin/jobs/%s/%s/' % (self.get_print_name(), id))
        except AssertionError:
            return HttpResponseBadRequest(
                "It's not possible to accept post: post is in a wrong state."
            )

    def reject(self, request, id):
        try:
            post = get_object_or_404(self.model, id=id)
            post.reject()
            messages.add_message(
                request,
                messages.INFO,
                '{0} is now rejected - an email to submitter was sent.'.format(
                    post.title
                )
            )
            return redirect('/admin/jobs/%s/%s/' % (self.get_print_name(), id))
        except AssertionError:
            return HttpResponseBadRequest(
                "It's not possible to reject reviewer: post is in a wrong state."
            )

    def restore(self, request, id):
        try:
            post = get_object_or_404(self.model, id=id)
            post.restore(request.user)
            messages.add_message(
                request,
                messages.INFO,
                '{0} is now restored.'.format(post.title)
            )
            return redirect('/admin/jobs/%s/%s/' % (self.get_print_name(), id))
        except AssertionError:
            return HttpResponseBadRequest(
                "It's not possible to restore post: post is in a wrong state."
            )

    def publish(self, request, id):
        try:
            post = get_object_or_404(self.model, id=id)
            post.publish()
            messages.add_message(
                request,
                messages.INFO,
                '{0} is now published - an email to submitter was sent.'.format(
                    post.title
                )
            )
            return redirect('/admin/jobs/%s/%s/' % (self.get_print_name(), id))
        except AssertionError:
            return HttpResponseBadRequest(
                "It's not possible to publish post: post is in a wrong state."
            )


class JobAdmin(PublishFlowModelAdmin):
    fieldsets = (
        ('Job info', {'fields': ('title', 'company', 'website', 'contact_email',
                           ('cities', 'country'), 'state_province', 'description', 'remote_work',
                           'relocation')}),
        ('Flow info', {'fields': ('review_status', 'message_to_organisation',
                                  'internal_comment', 'expiration_date',
                                  'reviewer', 'published_date')}),
    )
    readonly_fields = ('review_status', 'reviewer', 'published_date')
    list_display = ['title', 'company', 'reviewer', 'review_status', 'not_expired']
    list_filter = ('reviewer', 'review_status')
    ordering = ['title']
    actions = [make_published, send_status_update]
    formfield_overrides = {
        models.DateField: {'widget': SuitDateWidget},
        models.TextField: {'widget': AutosizedTextarea},
    }


class MeetupAdmin(PublishFlowModelAdmin):
    fieldsets = (
        ('Meetup info', {'fields': ('title', 'organisation', 'website',
                                    'contact_email', ('city', 'country'),
                                    'state_province', 'meetup_type', 'description', 'is_recurring',
                                    'recurrence', 'meetup_start_date',
                                    'meetup_end_date')}),
        ('Flow info', {'fields': ('review_status', 'message_to_organisation',
                                  'internal_comment', 'expiration_date',
                                  'reviewer', 'published_date')}),
    )
    readonly_fields = ('review_status', 'reviewer', 'published_date')
    list_display = ['title', 'city', 'reviewer', 'review_status', 'not_expired']
    list_filter = ('reviewer', 'review_status')
    ordering = ['title']
    actions = [make_published, send_status_update]
    formfield_overrides = {
        models.DateField: {'widget': SuitDateWidget},
        models.DateTimeField: {'widget': SuitSplitDateTimeWidget},
        models.TextField: {'widget': AutosizedTextarea},
    }


admin.site.register(Job, JobAdmin)
admin.site.register(Meetup, MeetupAdmin)
