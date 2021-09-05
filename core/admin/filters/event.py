from django.contrib import admin

from core.models import Event


class EventFilter(admin.SimpleListFilter):
    title = "Event"
    parameter_name = "event"

    def lookups(self, request, queryset):
        qs = Event.objects.all()
        if not request.user.is_superuser:
            qs = qs.filter(team__in=[request.user])
        return map(lambda x: (x.id, str(x)), qs)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(event=self.value())

        return queryset
