from django.contrib import admin, messages
from django.utils import timezone
from django.conf.urls import url
from django.shortcuts import redirect, get_object_or_404

from .models import EventApplication, Coorganizer
from .constants import ON_HOLD, IN_REVIEW, REJECTED, ACCEPTED


class InlineCoorganizerAdmin(admin.TabularInline):
    model = Coorganizer
    suit_classes = 'suit-tab suit-tab-organizers'
    extra = 1


def change_status_to_on_hold(modeladmin, request, queryset):
    queryset.update(status=ON_HOLD, status_changed_at=timezone.now())
change_status_to_on_hold.short_description = "Move selected application to on hold"


def change_status_to_in_review(modeladmin, request, queryset):
    queryset.update(status=IN_REVIEW, status_changed_at=timezone.now())
change_status_to_in_review.short_description = "Move selected application to in review"


@admin.register(EventApplication)
class EventApplicationAdmin(admin.ModelAdmin):
    raw_id_fields = ('previous_event', )
    actions = [change_status_to_on_hold, change_status_to_in_review]
    actions_on_top = True
    actions_on_bottom = False

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

    def get_urls(self):
        urls = super(EventApplicationAdmin, self).get_urls()
        my_urls = [
            url(r'(?P<application_id>\d+)/triage/(?P<new_status>[\w\d/]+)/$',
                self.admin_site.admin_view(self.view_change_application_status),
                name='organize_eventapplication_change_application_status'),
        ]
        return my_urls + urls

    def view_change_application_status(self, request, application_id, new_status):
        """
        Custom EventApplication admin view for handling triaging
        """
        application = get_object_or_404(EventApplication, id=application_id)

        if new_status in [IN_REVIEW, ON_HOLD]:
            application.status = new_status
            application.status_changed_at = timezone.now()
            application.save()
        elif new_status == REJECTED:
            application.reject()
        elif new_status == ACCEPTED:
            application.accept()
        else:
            messages.error(request, 'Invalid status provided for application')
            return redirect('admin:organize_eventapplication_change', application.id)

        messages.success(request, 'Application for {city}, {country} has been moved to {status}'.format(
            city=application.city,
            country=application.country,
            status=application.get_status_display()
        ))
        return redirect('admin:organize_eventapplication_changelist')
