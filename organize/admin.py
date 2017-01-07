from django.contrib import admin

from .models import EventApplication, Coorganizer


class InlineCoorganizerAdmin(admin.TabularInline):
    model = Coorganizer
    suit_classes = 'suit-tab suit-tab-organizers'
    extra = 1


@admin.register(EventApplication)
class EventApplicationAdmin(admin.ModelAdmin):
    raw_id_fields = ('previous_event', )
    list_display = (
        'city',
        'country',
        'date',
        'main_organizer',
        'status',
        'comment',
    )
    list_filter = ('status',)
    search_fields = (
        'city',
        'country',
        'main_organizer_first_name',
        'main_organizer_last_name',
        'main_organizer_email',
    )
    readonly_fields = (
        'status',
        'created_at',
        'status_changed_at',
        'about_you',
        'why',
        'involvement',
        'experience',
        'venue',
        'sponsorship',
        'coaches'
    )
    inlines = (InlineCoorganizerAdmin,)
    suit_form_tabs = (
        ('general', 'General'),
        ('application', 'Application'),
        ('organizers', 'Organizers')
    )
    fieldsets = (
        ('Application info', {
            'fields': [
                'status',
                'created_at',
                'status_changed_at',
                'comment'
            ],
            'classes': ('suit-tab', 'suit-tab-general',),
        }),
        ('Event info', {
            'fields': [
                'previous_event',
                'date',
                'city',
                'country',
                'website_slug',
            ],
            'classes': ('suit-tab', 'suit-tab-general',)
        }),
        ('Application', {
            'fields': [
                'about_you',
                'why',
                'involvement',
                'experience',
                'venue',
                'sponsorship',
                'coaches'
            ],
            'classes': ('suit-tab', 'suit-tab-application',)
        }),
        ('Main organizer', {
            'fields': [
                'main_organizer_email',
                'main_organizer_first_name',
                'main_organizer_last_name'
            ],
            'classes': ('suit-tab', 'suit-tab-organizers',)
        })
    )

    def main_organizer(self, obj):
        return "{} {} ({})".format(
            obj.main_organizer_first_name,
            obj.main_organizer_last_name,
            obj.main_organizer_email
        )
