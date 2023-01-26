from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import format_html

from core.models import Event

from .models import Answer, Application, Email, Form, Question


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("text_header", "event", "open_from", "open_until", "number_of_applications", "get_submissions_url")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(event__team__in=[request.user])

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            event = Event.objects.filter(team__in=[request.user])
            form.base_fields["event"].queryset = event
        return form

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("submissions/", self.admin_site.admin_view(self.view_submissions)),
        ]
        return my_urls + urls

    def view_submissions(self, request):
        forms = self.get_queryset(request)
        if forms.count() == 1:
            # There is only one form, redirect to applications list straight away
            form = forms.get()
            return redirect("applications:applications", form.event.page_url)
        return render(request, "admin/applications/form/view_submissions.html", {"forms": forms})

    @admin.display(description="Applications")
    def get_submissions_url(self, obj):
        return format_html(
            '<a href="{}" target="_blank">See all submitted applications</a>',
            reverse("applications:applications", args=[obj.event.page_url]),
        )


class FormFilter(admin.SimpleListFilter):
    title = "Form"
    parameter_name = "form"

    def lookups(self, request, queryset):
        qs = Form.objects.all()
        if not request.user.is_superuser:
            qs = qs.filter(event__team__in=[request.user])
        return map(lambda x: (x.id, str(x)), qs)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(form=self.value())

        return queryset


@admin.register(Question)
class QuestionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("form", "title", "question_type", "is_required", "order")
    list_filter = (FormFilter,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(form__event__team__in=[request.user])

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form_objs = Form.objects.filter(event__team__in=[request.user])
            form.base_fields["form"].queryset = form_objs
        return form


class AnswerInlineAdmin(admin.TabularInline):
    model = Answer
    can_delete = False
    extra = 0
    readonly_fields = ("question", "answer")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("number", "form", "newsletter_optin", "email", "created")
    list_filter = ("form", "newsletter_optin")
    inlines = [AnswerInlineAdmin]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("application", "question", "answer")
    raw_id_fields = ("question", "application")


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("form", "author", "subject", "recipients_group", "created", "sent")
