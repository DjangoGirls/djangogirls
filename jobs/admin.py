from django.db import models
from django.contrib import admin
from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget, AutosizedTextarea

from .models import PublishFlowModel, Job, Meetup


def make_published(modeladmin, request, queryset):
    for item in queryset:
        if item.review_status == PublishFlowModel.READY_TO_PUBLISH:
            item.publish()
make_published.short_description = "Publish selected items"


class JobAdmin(admin.ModelAdmin):
    readonly_fields = ('published_date',)
    list_display = ['title', 'company', 'reviewer', 'review_status']
    ordering = ['title']
    actions = [make_published]
    formfield_overrides = {
        models.DateField: {'widget': SuitDateWidget},
        models.TextField: {'widget': AutosizedTextarea},
    }


class MeetupAdmin(admin.ModelAdmin):
    readonly_fields = ('published_date',)
    list_display = ['title', 'city', 'reviewer', 'review_status']
    ordering = ['title']
    actions = [make_published]
    formfield_overrides = {
        models.DateField: {'widget': SuitDateWidget},
        models.DateTimeField: {'widget': SuitSplitDateTimeWidget},
        models.TextField: {'widget': AutosizedTextarea},
    }


admin.site.register(Job, JobAdmin)
admin.site.register(Meetup, MeetupAdmin)
