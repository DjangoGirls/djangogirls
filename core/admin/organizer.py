from django.contrib import admin, messages
from django.shortcuts import get_object_or_404
from django.urls import path
from django.utils.translation import gettext_lazy as _
from models.organizer import OrganizerIssue


@admin.register(OrganizerIssue)
class OrganizerIssueAdmin(admin.ModelAdmin):
    list_display = (
        "organizer",
        "event",
        "date_reported",
        "reported_by",
        "issue_handled",
        "issue_handled_by",
        "last_updated",
    )
    list_filter = (
        "organizer",
        "event",
        "reported_by",
    )
    search_fields = (
        "organizer",
        "event",
        "reported_by",
    )

    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path(
                "<int:organizerissue_id>/blacklist_organizer/",
                self.admin_site.admin_view(self.blacklist_organizer),
                name="core_organizer_blacklist_organizer",
            ),
        ]

        return my_urls + urls

    def blacklist_organizer(self, request, organizerissue_id):
        organizer = get_object_or_404(OrganizerIssue, id=organizerissue_id)
        organizer.blacklist_organizer()
        messages.success(
            request,
            _("Organizer %(organizer)s, of %(event)s has been blackliste.")
            % {"organizer": f"{organizer.organizer.get_full_name()}", "event": organizer.event},
        )
