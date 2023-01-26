from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from core.admin.filters.event import EventFilter
from core.models import Event


class EventPageMenuAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("title", "event", "url", "position")
    list_filter = (EventFilter,)
    sortable = "position"

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
