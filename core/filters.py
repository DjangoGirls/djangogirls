from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class OpenRegistrationFilter(admin.SimpleListFilter):
    title = _("Open registration")
    parameter_name = "open_registration"

    def lookups(self, request, model_admin):
        return (("open", _("Show events with open registration")),)

    def queryset(self, request, queryset):
        if self.value() == "open":
            now = timezone.now()
            return queryset.filter(form__open_from__lte=now, form__open_until__gte=now)
