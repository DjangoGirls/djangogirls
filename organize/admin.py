from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .constants import ACCEPTED, DEPLOYED, IN_REVIEW, NEW, ON_HOLD, REJECTED
from .models import Coorganizer, EventApplication

ANONYMOUS_STATUSES = (NEW, IN_REVIEW)
IDENTITY_FIELDS = (
    "previous_event",
    "city",
    "country",
    "website_slug",
    "main_organizer_email",
    "main_organizer_first_name",
    "main_organizer_last_name",
)
REVEALED_SESSION_KEY = "revealed_event_applications"
CHANGE_URL_NAME = "admin:organize_eventapplication_change"


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
        "display_city",
        "display_country",
        "date",
        "created_at",
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
        "organizer_blacklisted",
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
                "fields": [
                    "main_organizer_email",
                    "main_organizer_first_name",
                    "main_organizer_last_name",
                    "organizer_blacklisted",
                ],
                "classes": (
                    "suit-tab",
                    "suit-tab-organizers",
                ),
            },
        ),
    )

    def is_anonymous(self, request, obj):
        return obj.status in ANONYMOUS_STATUSES and obj.pk not in request.session.get(REVEALED_SESSION_KEY, [])

    def anonymous_label(self, obj):
        return _("Application #%(id)s") % {"id": obj.pk}

    @admin.display(description=_("City"))
    def display_city(self, obj):
        return self.anonymous_label(obj) if obj.status in ANONYMOUS_STATUSES else obj.city

    @admin.display(description=_("Country"))
    def display_country(self, obj):
        return _("Hidden") if obj.status in ANONYMOUS_STATUSES else obj.get_country_display()

    @admin.display(description=_("Main organizer"))
    def main_organizer(self, obj):
        if obj.status in ANONYMOUS_STATUSES:
            return _("Hidden")
        return f"{obj.main_organizer_first_name} {obj.main_organizer_last_name} ({obj.main_organizer_email})"

    def get_search_results(self, request, queryset, search_term):
        if search_term:
            queryset = queryset.exclude(status__in=ANONYMOUS_STATUSES)
        return super().get_search_results(request, queryset, search_term)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not obj or not self.is_anonymous(request, obj):
            return fieldsets
        return [
            (name, {**options, "fields": [field for field in options["fields"] if field not in IDENTITY_FIELDS]})
            for name, options in fieldsets
        ]

    def get_inlines(self, request, obj):
        if obj and self.is_anonymous(request, obj):
            return ()
        return super().get_inlines(request, obj)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and self.is_anonymous(request, obj):
            label = self.anonymous_label(obj)
            extra_context = {**(extra_context or {}), "anonymous_label": label, "subtitle": label}
        return super().change_view(request, object_id, form_url, extra_context)

    def view_reveal_application(self, request, application_id):
        application = get_object_or_404(EventApplication, id=application_id)
        if not self.has_view_permission(request, application):
            raise PermissionDenied
        revealed = request.session.get(REVEALED_SESSION_KEY, [])
        if application.pk not in revealed:
            request.session[REVEALED_SESSION_KEY] = [*revealed, application.pk]
        return redirect(CHANGE_URL_NAME, application.id)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "<int:application_id>/reveal/",
                self.admin_site.admin_view(self.view_reveal_application),
                name="organize_eventapplication_reveal",
            ),
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
            return redirect(CHANGE_URL_NAME, application.id)
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
            return redirect(CHANGE_URL_NAME, application.id)

        status = application.get_status_display()
        if self.is_anonymous(request, application):
            label = self.anonymous_label(application)
            message = _("%(application)s has been moved to %(status)s") % {"application": label, "status": status}
        else:
            message = _("Application for %(city)s, %(country)s has been moved to %(status)s") % {
                "city": application.city,
                "country": application.country,
                "status": status,
            }
        messages.success(request, message)

        return redirect("admin:organize_eventapplication_changelist")
