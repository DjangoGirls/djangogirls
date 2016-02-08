from django.contrib import admin
from django.utils import timezone


class OpenRegistrationFilter(admin.SimpleListFilter):
    title = 'Open registration'
    parameter_name = 'open_registration'

    def lookups(self, request, model_admin):
        return (
            ('open', 'Show events with open registration'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'open':
            now = timezone.now()
            return queryset.filter(eventpage__form__open_from__lte=now,
                                   eventpage__form__open_until__gte=now)
