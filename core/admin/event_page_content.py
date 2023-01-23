from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from coach.admin import CoachInline
from core.admin.filters.event import EventFilter
from core.admin.forms.event_page_content import EventPageContentForm
from core.models import Event
from sponsor.admin import SponsorInline


class EventPageContentAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "event", "position", "is_public")
    list_filter = (EventFilter, "is_public")
    search_fields = ("name", "event__page_title", "content", "event__city", "event__country", "event__name")
    form = EventPageContentForm
    sortable = "position"
    inlines = [SponsorInline, CoachInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(event__team=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if "event" in form.base_fields:
                form.base_fields["event"].queryset = Event.objects.filter(team=request.user)
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            # Don't let change objects for events that already happened
            if not obj.event.is_upcoming():
                return {x.name for x in self.model._meta.fields}
        return self.readonly_fields
