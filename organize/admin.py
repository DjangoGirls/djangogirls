from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .constants import ACCEPTED, DEPLOYED, IN_REVIEW, ON_HOLD, REJECTED
from .models import Coorganizer, EventApplication


class InlineCoorganizerAdmin(admin.TabularInline):
    model = Coorganizer
    suit_classes = "suit-tab suit-tab-organizers"
    extra = 1


@admin.action(description=_("Move selected application to on hold"))
def change_status_to_on_hold(modeladmin, request, queryset):
    queryset.change_status_to(ON_HOLD)


@admin.action(description=_("Move selected application to in review"))
def change_status_to_in_review(modeladmin, request, queryset):
    queryset.change_status_to(IN_REVIEW)


@admin.register(EventApplication)
class EventApplicationAdmin(admin.ModelAdmin):
    raw_id_fields = ("previous_event",)
    actions = [change_status_to_on_hold, change_status_to_in_review]
    actions_on_top = True
    actions_on_bottom = False

    list_display = (
        "city",
        "country",
        "date",
        "main_organizer",
        "status",
        "comment",
    )
    list_filter = ("status",)
    search_fields = (
        "city",
        "country",
        "main_organizer_first_name",
        "main_organizer_last_name",
        "main_organizer_email",
    )
    readonly_fields = (
        "status",
        "created_at",
        "status_changed_at",
        "about_you",
        "why",
        "involvement",
        "experience",
        "venue",
        "sponsorship",
        "coaches",
        "remote",
        "tools",
        "local_restrictions",
        "safety",
        "diversity",
        "additional",
        "confirm_covid_19_protocols",
    )
    inlines = (InlineCoorganizerAdmin,)
    suit_form_tabs = (  # TODO: Can this be changed into something still useful?
        ("general", "General"),
        ("application", "Application"),
        ("organizers", "Organizers"),
    )
    fieldsets = (
        (
            _("Application info"),
            {
                "fields": ["status", "created_at", "status_changed_at", "comment"],
                "classes": (
                    "suit-tab",
                    "suit-tab-general",
                ),
            },
        ),
        (
            _("Event info"),
            {
                "fields": [
                    "previous_event",
                    "date",
                    "city",
                    "country",
                    "website_slug",
                ],
                "classes": (
                    "suit-tab",
                    "suit-tab-general",
                ),
            },
        ),
        (
            _("Application"),
            {
                "fields": [
                    "about_you",
                    "why",
                    "involvement",
                    "experience",
                    "venue",
                    "sponsorship",
                    "coaches",
                    "remote",
                    "tools",
                    "local_restrictions",
                    "safety",
                    "diversity",
                    "additional",
                    "confirm_covid_19_protocols",
                ],
                "classes": (
                    "suit-tab",
                    "suit-tab-application",
                ),
            },
        ),
        (
            _("Main organizer"),
            {
                "fields": ["main_organizer_email", "main_organizer_first_name", "main_organizer_last_name"],
                "classes": (
                    "suit-tab",
                    "suit-tab-organizers",
                ),
            },
        ),
    )

    def main_organizer(self, obj):
        return f"{obj.main_organizer_first_name} {obj.main_organizer_last_name} ({obj.main_organizer_email})"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "<int:application_id>/triage/<str:new_status>/",
                self.admin_site.admin_view(self.view_change_application_status),
                name="organize_eventapplication_change_application_status",
            ),
        ]
        return my_urls + urls

    def view_change_application_status(self, request, application_id, new_status):
        """
        Custom EventApplication admin view for handling triaging
        """
        application = get_object_or_404(EventApplication, id=application_id)

        if application.status is DEPLOYED:
            messages.error(request, _("The application is already deployed"))
            return redirect("admin:organize_eventapplication_change", application.id)
        elif new_status in [IN_REVIEW, ON_HOLD]:
            application.change_status_to(new_status)
        elif new_status in [REJECTED, ACCEPTED]:
            if request.method == "GET":
                return render(
                    request,
                    "admin/organize/eventapplication/view_change_status.html",
                    {"application": application, "new_status": new_status},
                )
            elif request.method == "POST":
                if new_status == REJECTED:
                    application.reject()
                else:
                    event = application.deploy()
                    if event:
                        # deploy returns None if it is already deployed
                        application.send_deployed_email(event)
        else:
            messages.error(request, _("Invalid status provided for application"))
            return redirect("admin:organize_eventapplication_change", application.id)

        messages.success(
            request,
            _("Application for %(city)s, %(country)s has been moved to %(status)s")
            % {"city": application.city, "country": application.country, "status": application.get_status_display()},
        )

        return redirect("admin:organize_eventapplication_changelist")
