from datetime import datetime

from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from ..filters import OpenRegistrationFilter
from ..forms import AddOrganizerForm, EventForm
from ..models import Event


@admin.action(description="Clone selected Events")
def clone_action(modeladmin, request, queryset):
    """
    Clone the selected Events, making a copy of the Event.
    """
    count = 0
    for event in queryset:
        event.clone()
        count += 1

    messages.success(request, "{} event{} cloned".format(count, "" if count == 1 else "s"))


@admin.action(description="Freeze selected Events")
def freeze_action(modeladmin, request, queryset):
    """
    Freeze selected events, making the event website inaccessible the same way it
    would be if it is not yet live.
    """
    count = 0
    for event in queryset:
        event.freeze()
        count += 1

    messages.success(request, "{} event{} frozen".format(count, "" if count == 1 else "s"))


@admin.action(description="Unfreeze selected events")
def unfreeze_action(modeladmin, request, queryset):
    """
    Unfreeze selected events, making the  event website accessible the same way it
    would be if it is live.
    """
    count = 0
    for event in queryset:
        event.unfreeze()
        count += 1

    messages.success(request, "{} event{} unfrozen".format(count, "" if count == 1 else "s"))


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organizers",
        "email",
        "date",
        "city",
        "country",
        "is_on_homepage",
        "is_past_event",
        "has_stats",
        "is_frozen",
    )
    list_filter = (OpenRegistrationFilter,)
    search_fields = ("city", "country", "name")
    filter_horizontal = ["team"]
    actions = [clone_action, freeze_action, unfreeze_action]
    form = EventForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(team=request.user)

    @admin.display(
        description=_("past event?"),
        boolean=True,
    )
    def is_past_event(self, obj):
        return not obj.is_upcoming()

    @admin.display(
        description=_("has stats?"),
        boolean=True,
    )
    def has_stats(self, obj):
        return obj.has_stats

    @admin.display(description=_("page URL"))
    def full_url(self, obj):
        url = reverse("core:event", kwargs={"page_url": obj.page_url})
        url = f"https://djangogirls.org{url}"
        return mark_safe('<a href="{url}">{url}</a>'.format(url=url))

    def get_readonly_fields(self, request, obj=None):
        fields = set(self.readonly_fields) | {"full_url"}
        if obj and not request.user.is_superuser:
            fields.update({"city", "country", "email", "is_on_homepage", "name", "page_url", "team"})
            # Don't let change objects for events that already happened
            if not obj.is_upcoming():
                fields.update({x.name for x in self.model._meta.fields})
                fields.difference_update({"attendees_count", "applicants_count"})
        return fields

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return [
                (
                    _("Event info"),
                    {
                        "fields": [
                            "name",
                            "date",
                            "city",
                            "country",
                            "latlng",
                            "email",
                            "page_url",
                            "is_deleted",
                            "is_frozen",
                        ]
                    },
                ),
                (_("Event main picture"), {"fields": ["photo", "photo_credit", "photo_link", "is_on_homepage"]}),
                (_("Team"), {"fields": ["main_organizer", "team"]}),
                (
                    _("Event website"),
                    {
                        "fields": [
                            "page_title",
                            "page_description",
                            "page_main_color",
                            "page_custom_css",
                            "is_page_live",
                        ]
                    },
                ),
                (
                    _("Statistics"),
                    {
                        "fields": [
                            "applicants_count",
                            "attendees_count",
                        ]
                    },
                ),
            ]
        return [
            (_("Event info"), {"fields": ["name", "date", "city", "country", "full_url"]}),
            (
                _("Event main picture"),
                {
                    "fields": [
                        "photo",
                        "photo_credit",
                        "photo_link",
                    ]
                },
            ),
            (
                _("Event website"),
                {"fields": ["page_title", "page_description", "page_main_color", "page_custom_css", "is_page_live"]},
            ),
            (
                _("Statistics"),
                {
                    "fields": [
                        "applicants_count",
                        "attendees_count",
                    ]
                },
            ),
        ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "manage_organizers/",
                self.admin_site.admin_view(self.view_manage_organizers),
                name="core_event_manage_organizers",
            ),
            path(
                "add_organizers/",
                self.admin_site.admin_view(self.view_add_organizers),
                name="core_event_add_organizers",
            ),
        ]
        return my_urls + urls

    def _get_future_events_for_user(self, request):
        """
        Retrieves a list of future events, ordered by name.
        It's based on get_queryset, so superuser see all events, while
        is_staff users see events they're assigned to only.
        """
        return self.get_queryset(request).filter(date__gte=datetime.now().strftime("%Y-%m-%d")).order_by("name")

    def _get_event_from_get(self, request, all_events):
        """
        Retrieves a particular event from request.GET['event_id'], or
        returns the first one from all events available to the user.
        """
        if "event_id" in request.GET:
            try:
                return all_events.get(id=request.GET["event_id"])
            except Event.DoesNotExist:
                pass
        else:
            return all_events.first()

    def view_manage_organizers(self, request):
        """
        Custom admin view that allows user to remove organizers from an event
        """
        all_events = self._get_future_events_for_user(request)
        event = self._get_event_from_get(request, all_events)

        if "remove" in request.GET and event in all_events:
            from core.models import User

            user = User.objects.get(id=request.GET["remove"])
            if user == request.user:
                messages.error(request, _("You cannot remove yourself from a team."))
            else:
                if user in event.team.all():
                    event.team.remove(user)
                    messages.success(
                        request, _("Organizer %(user_name)s has been removed") % {"user_name": user.get_full_name()}
                    )
                    return HttpResponseRedirect(reverse("admin:core_event_manage_organizers") + f"?event_id={event.id}")

        return render(
            request,
            "admin/core/event/view_manage_organizers.html",
            {
                "all_events": all_events,
                "event": event,
                "title": _("Remove organizers"),
            },
        )

    def view_add_organizers(self, request):
        """
        Custom admin view that allows user to add new organizer to an event
        """
        all_events = self._get_future_events_for_user(request)
        event = self._get_event_from_get(request, all_events)

        if request.method == "POST":
            form = AddOrganizerForm(request.POST, event_choices=all_events)
            if form.is_valid():
                user = form.save()
                messages.success(
                    request,
                    _(
                        "%(user_name)s has been added to your event, yay! They've been also"
                        " invited to Slack and should receive credentials to login"
                        " in an e-mail."
                    )
                    % {"user_name": user.get_full_name()},
                )
                return redirect("admin:core_event_add_organizers")
        else:
            form = AddOrganizerForm(event_choices=all_events)

        return render(
            request,
            "admin/core/event/view_add_organizers.html",
            {
                "all_events": all_events,
                "event": event,
                "form": form,
                "title": _("Add organizers"),
            },
        )

    def save_model(self, request, obj, form, change):
        created = not obj.pk
        super().save_model(request, obj, form, change)
        if created:
            obj.add_default_content()
            obj.add_default_menu()
