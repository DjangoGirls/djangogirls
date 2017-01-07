from django.contrib import admin

from .models import EventApplication, Coorganizer


class InlineCoorganizerAdmin(admin.TabularInline):
    model = Coorganizer
    extra = 1


@admin.register(EventApplication)
class EventApplicationAdmin(admin.ModelAdmin):
    list_display = ('city', 'country', 'date')
    inlines = (InlineCoorganizerAdmin,)
