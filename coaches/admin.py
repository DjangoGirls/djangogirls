from django.contrib import admin

from suit.admin import SortableModelAdmin

from .models import CoachForm, Question, CoachApplication, Answer, CoachEmail
from core.models import EventPage


class FormAdmin(admin.ModelAdmin):
    list_display = (
        'text_header', 'page', 'text_description',
        'open_from', 'open_until', 'number_of_applications')

    def get_queryset(self, request):
        qs = super(FormAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(page__event__team__in=[request.user])

    def get_form(self, request, obj=None, **kwargs):
        form = super(FormAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            page = EventPage.objects.filter(event__team__in=[request.user])
            form.base_fields['page'].queryset = page
        return form


class QuestionAdmin(SortableModelAdmin):
    list_display = ('form', 'title', 'question_type', 'is_required', 'order')
    sortable = 'order'

    def get_queryset(self, request):
        qs = super(QuestionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(form__page__event__team__in=[request.user])

    def get_form(self, request, obj=None, **kwargs):
        form = super(QuestionAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form_objs = CoachForm.objects.filter(page__event__team__in=[request.user])
            form.base_fields['form'].queryset = form_objs
        return form


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('number', 'form', 'email', 'created')
    list_filter = ('form', )


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('application', 'question', 'answer')
    raw_id_fields = ('question', 'application')


class EmailAdmin(admin.ModelAdmin):
    list_display = ('form', 'author', 'subject', 'recipients_group', 'created', 'sent')


admin.site.register(CoachForm, FormAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(CoachApplication, ApplicationAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(CoachEmail, EmailAdmin)
