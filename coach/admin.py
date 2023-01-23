from django.contrib import admin

from coach.models import Coach
from core.models import EventPageContent


class CoachInline(admin.TabularInline):
    model = EventPageContent.coaches.through
    extra = 1
    verbose_name_plural = "Coaches"


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ("name", "photo_display_for_admin", "twitter_handle", "url")
    search_fields = ("name", "twitter_handle", "url")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(eventpagecontent__event__team=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if "eventpagecontent" in form.base_fields:
                qs = EventPageContent.objects.filter(event__team=request.user)
                form.base_fields["eventpagecontent"].queryset = qs
        return form
