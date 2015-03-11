from django.contrib import admin

from suit.admin import SortableModelAdmin

from .models import Form, Question, Application, Answer
from core.models import EventPage


class FormAdmin(admin.ModelAdmin):
    list_display = ('text_header', 'page', 'text_description', 'open_from', 'open_until', 'number_of_applications')

    def get_queryset(self, request):
        qs = super(FormAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(page__event__team__in=[request.user,])

    def get_form(self, request, obj=None, **kwargs):
        form = super(FormAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['page'].queryset = EventPage.objects.filter(event__team__in=[request.user])
        return form


class QuestionAdmin(SortableModelAdmin):
    list_display = ('form', 'title', 'question_type', 'is_required', 'order')
    sortable = 'order'

    def get_queryset(self, request):
        qs = super(QuestionAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(form__page__event__team__in=[request.user,])

    def get_form(self, request, obj=None, **kwargs):
        form = super(QuestionAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['form'].queryset = Form.objects.filter(page__event__team__in=[request.user])
        return form


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('form', 'created')

    def get_queryset(self, request):
        qs = super(ApplicationAdmin, self).queryset(request)
        return qs.filter(form__page__event__team__in=[request.user,])


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('application', 'question', 'answer')
    raw_id_fields = ('question', 'application')

    def get_queryset(self, request):
        qs = super(AnswerAdmin, self).queryset(request)
        return qs.filter(application__form__page__event__team__in=[request.user,])


admin.site.register(Form, FormAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Answer, AnswerAdmin)
