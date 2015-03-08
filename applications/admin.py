from django.contrib import admin

from suit.admin import SortableModelAdmin

from .models import Form

class FormAdmin(admin.ModelAdmin):
    list_display = ('text_header', 'page', 'text_description', 'open_from', 'open_until')

    def get_queryset(self, request):
        qs = super(FormAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(page__event__team__in=[request.user,])

    def get_form(self, request, obj=None, **kwargs):
        form = super(FormAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['page'].queryset = FormAdmin.objects.filter(event__team__in=[request.user])
        return form



admin.site.register(Form, FormAdmin)
