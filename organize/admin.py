from django.contrib import admin

from .models import EventApplication, Team


class InlineTeamAdmin(admin.TabularInline):
    model = Team
    extra = 1


@admin.register(EventApplication)
class EventApplicationAdmin(admin.ModelAdmin):
    list_display = ('city', 'country', 'date')
    inlines = (InlineTeamAdmin,)
