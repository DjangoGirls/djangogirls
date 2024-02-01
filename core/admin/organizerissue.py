from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import path
from django.utils.translation import gettext_lazy as _

from core.models.organizerissue import OrganizerIssue

from .forms.organizerissue import OrganizerIssueForm


class OrganizerIssueAdmin(admin.ModelAdmin):
    form = OrganizerIssueForm
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
                "<int:organizerissue_id>/triage/blacklist/",
                self.admin_site.admin_view(self.blacklist),
                name="core_organizerissue_blacklist",
            ),
            path(
                "<int:organizerissue_id>/triage/reverse_blacklist/",
                self.admin_site.admin_view(self.reverse_blacklist),
                name="core_organizerissue_reverse_blacklist",
            ),
        ]
        return my_urls + urls

    def blacklist(self, request, organizerissue_id):
        organizer = get_object_or_404(OrganizerIssue, id=organizerissue_id)
        organizer.blacklist_organizer()
        messages.success(
            request,
            _("Organizer %(organizer)s, of %(event)s has been blacklisted.")
            % {"organizer": f"{organizer.organizer.get_full_name()}", "event": organizer.event},
        )
        return redirect("admin:core_organizerissue_changelist")

    def reverse_blacklist(self, request, organizerissue_id):
        organizer = get_object_or_404(OrganizerIssue, id=organizerissue_id)
        organizer.reverse_blacklist_organizer()
        messages.success(
            request,
            _("Blacklisting for organizer %(organizer)s, of %(event)s has been reversed.")
            % {"organizer": f"{organizer.organizer.get_full_name()}", "event": organizer.event},
        )
        return redirect("admin:core_organizerissue_changelist")
