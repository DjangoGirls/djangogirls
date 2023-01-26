from django.contrib import admin

from .models import Company, Job


class CompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("name",),
    }
    search_fields = ("name",)


class JobAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "location", "remuneration", "open", "date_created")
    search_fields = ("company", "role")
    list_filter = ("open", "company", "location", "date_created")


admin.site.register(Company, CompanyAdmin)
admin.site.register(Job, JobAdmin)
