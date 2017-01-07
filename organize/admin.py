from django.contrib import admin

from .models import EventApplication, Coorganizer


class InlineCoorganizerAdmin(admin.TabularInline):
    model = Coorganizer
    extra = 1


@admin.register(EventApplication)
class EventApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'city',
        'country',
        'date',
        'main_organizer',
        'status',
        'comment',
    )
    inlines = (InlineCoorganizerAdmin,)

    def main_organizer(self, obj):
        return "{} {} ({})".format(
            obj.main_organizer_first_name,
            obj.main_organizer_last_name,
            obj.main_organizer_email
        )
