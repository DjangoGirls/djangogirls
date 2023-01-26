from django.contrib import admin

from core.models import EventPageContent

from .models import Donor, Sponsor


class SponsorInline(admin.TabularInline):
    model = EventPageContent.sponsors.through
    extra = 1
    verbose_name_plural = "Sponsors"


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "logo_display_for_admin", "url")
    list_per_page = 50
    search_fields = ("name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(eventpagecontent__event__team=request.user).distinct()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if "eventpagecontent" in form.base_fields:
                qs = EventPageContent.objects.filter(event__team=request.user)
                form.base_fields["eventpagecontent"].queryset = qs
        return form


admin.site.register(Donor)
