from django.contrib import admin
from django.forms import ModelForm
from django.contrib.auth import admin as auth_admin

from suit_redactor.widgets import RedactorWidget
from suit.admin import SortableModelAdmin, SortableTabularInline

from .models import *
from .forms import UserChangeForm, UserCreationForm, UserLimitedChangeForm


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'organizers', 'date', 'city', 'country', 'is_on_homepage', 'is_past_event', 'has_stats')
    search_fields = ('city', 'country', 'name')

    def get_queryset(self, request):
        qs = super(EventAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(team=request.user)

    def is_past_event(self, obj):
        return not obj.is_upcoming()
    is_past_event.boolean = True

    def has_stats(self, obj):
        return Postmortem.objects.filter(event=obj).exists()
    has_stats.boolean = True


class EventPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'is_live')
    search_fields = ('title', 'event__name', 'event__city', 'event__country')

    def get_queryset(self, request):
        qs = super(EventPageAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(event__team=request.user)

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            # Don't let change objects for events that already happened
            if not obj.event.is_upcoming():
                return set([x.name for x in self.model._meta.fields])
        return self.readonly_fields


class EventPageContentForm(ModelForm):
    class Meta:
        widgets = {
            'content': RedactorWidget(editor_options={'lang': 'en'})
        }


class SponsorInline(SortableTabularInline):
    model = Sponsor
    extra = 1
    verbose_name_plural = 'Sponsors'
    sortable = 'position'
    fields = ('name', 'logo', 'url', 'position')


class CoachInline(admin.TabularInline):
    model = Coach
    extra = 1
    verbose_name_plural = 'Coaches'
    sortable = 'position'
    fields = ('name', 'twitter_handle', 'url', 'photo')


class EventPageContentAdmin(SortableModelAdmin):
    list_display = ('name', 'page', 'content', 'position', 'is_public')
    list_filter = ('page', 'is_public')
    search_fields = ('name', 'page__title', 'content', 'page__event__city',
                     'page__event__country', 'page__event__name')
    form = EventPageContentForm
    sortable = 'position'
    inlines = [
        SponsorInline,
        CoachInline
    ]

    def get_queryset(self, request):
        qs = super(EventPageContentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(page__event__team=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super(EventPageContentAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if 'page' in form.base_fields:
                form.base_fields['page'].queryset = EventPage.objects.filter(
                    event__team=request.user
                )
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            # Don't let change objects for events that already happened
            if not obj.page.event.is_upcoming():
                return set([x.name for x in self.model._meta.fields])
        return self.readonly_fields


class EventPageMenuAdmin(SortableModelAdmin):
    list_display = ('title', 'page', 'url', 'position')
    list_filter = ('page',)
    sortable = 'position'

    def get_queryset(self, request):
        qs = super(EventPageMenuAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(page__event__team=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super(EventPageMenuAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if 'page' in form.base_fields:
                form.base_fields['page'].queryset = EventPage.objects.filter(
                    event__team=request.user
                )
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            # Don't let change objects for events that already happened
            if not obj.page.event.is_upcoming():
                return set([x.name for x in self.model._meta.fields])
        return self.readonly_fields


class SponsorAdmin(SortableModelAdmin):
    list_display = ('name', 'logo_display_for_admin', 'url', 'position')
    list_filter = ('event_page_content__page',)
    sortable = 'position'

    def get_queryset(self, request):
        qs = super(SponsorAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(event_page_content__page__event__team=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super(SponsorAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if 'event_page_content' in form.base_fields:
                qs = EventPageContent.objects.filter(page__event__team=request.user)
                form.base_fields['event_page_content'].queryset = qs
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            # Don't let change objects for events that already happened
            if not obj.event_page_content.page.event.is_upcoming():
                return set([x.name for x in self.model._meta.fields])
        return self.readonly_fields


class CoachAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo_display_for_admin', 'twitter_handle', 'url')
    list_filter = ('event_page_content__page',)

    def get_queryset(self, request):
        qs = super(CoachAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(event_page_content__page__event__team=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super(CoachAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if 'event_page_content' in form.base_fields:
                qs = EventPageContent.objects.filter(page__event__team=request.user)
                form.base_fields['event_page_content'].queryset = qs
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            # Don't let change objects for events that already happened
            if not obj.event_page_content.page.event.is_upcoming():
                return set([x.name for x in self.model._meta.fields])
        return self.readonly_fields


class PostmortemAdmin(admin.ModelAdmin):
    list_display = ('event', 'attendees_count', 'applicants_count')


class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    limited_fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    form = UserChangeForm
    limited_form = UserLimitedChangeForm
    add_form = UserCreationForm
    change_password_form = auth_admin.AdminPasswordChangeForm
    list_display = ('email', 'first_name', 'last_name', 'is_superuser')
    list_filter = ('event', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined',)

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.pk)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj and not request.user.is_superuser:
            defaults.update({
                'form': self.limited_form,
                'fields': admin.util.flatten_fieldsets(self.limited_fieldsets),
            })
        defaults.update(kwargs)
        return super(UserAdmin, self).get_form(request, obj, **defaults)

    def get_fieldsets(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return self.limited_fieldsets
        return super(UserAdmin, self).get_fieldsets(request, obj)

admin.site.register(Event, EventAdmin)
admin.site.register(EventPage, EventPageAdmin)
admin.site.register(EventPageContent, EventPageContentAdmin)
admin.site.register(EventPageMenu, EventPageMenuAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Postmortem, PostmortemAdmin)
admin.site.register(Coach, CoachAdmin)
