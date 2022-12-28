from django.contrib import admin

from .models import Company, Job


admin.site.register(Company)


class JobAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'location', 'remuneration', 'open', 'date_created')
    search_fields = ('company', 'role')
    list_filter = ('open', 'company')


admin.site.register(Job, JobAdmin)
