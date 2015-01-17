from django.contrib import admin

from .models import Company, Job


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
    for job in queryset:
        job.publish()
    queryset.update()
make_published.short_description = "Mark selected as published"

class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'reviewer', 'published']
    ordering = ['title']
    actions = [make_published]

admin.site.register(Company)
admin.site.register(Job, JobAdmin)


