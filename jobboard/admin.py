from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "location", "remuneration", "open", "date_created")
    search_fields = ("company", "role")
    list_filter = ("open", "company", "location", "date_created")
