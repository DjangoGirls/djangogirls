from django.contrib import admin

from .models import Company, Job


def make_published(modeladmin, request, queryset):
    queryset.update(ready_to_publish=True)
    for job in queryset:
        job.publish()
        job.set_expiration_date()
    queryset.update()
make_published.short_description = "Mark selected as published"


class JobAdmin(admin.ModelAdmin):
    readonly_fields = ('published_date',)
    list_display = ['title', 'company', 'reviewer', 'ready_to_publish']
    ordering = ['title']
    actions = [make_published]

admin.site.register(Company)
admin.site.register(Job, JobAdmin)
