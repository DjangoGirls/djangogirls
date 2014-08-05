from django.contrib import admin
from django.forms import ModelForm
from django.contrib.auth import admin as auth_admin
from forms import UserChangeForm, UserCreationForm, UserLimitedChangeForm
from suit_redactor.widgets import RedactorWidget
from suit.admin import SortableModelAdmin

from .models import *

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'city', 'country', 'is_on_homepage')
    search_fields = ('city', 'country')

    def queryset(self, request):
        qs = super(EventAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(team__in=[request.user,])

class EventPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'is_live')

    def queryset(self, request):
        qs = super(EventPageAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(event__team__in=[request.user,])

class EventPageContentForm(ModelForm):
    class Meta:
        widgets = {
            'content': RedactorWidget(editor_options={'lang': 'en'})
        }

class EventPageContentAdmin(SortableModelAdmin):
    list_display = ('name', 'page', 'content', 'position', 'is_public')
    list_filter = ('page','is_public')
    form = EventPageContentForm
    sortable = 'position'

    def queryset(self, request):
		qs = super(EventPageContentAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(page__event__team__in=[request.user,])

    def get_form(self, request, obj=None, **kwargs):
		form = super(EventPageContentAdmin, self).get_form(request, obj, **kwargs)
		if not request.user.is_superuser:
			form.base_fields['page'].queryset = EventPage.objects.filter(event__team__in=[request.user])
		return form

class EventPageMenuAdmin(SortableModelAdmin):
    list_display = ('title', 'page', 'url', 'position')
    list_filter = ('page',)
    sortable = 'position'

    def queryset(self, request):
        qs = super(EventPageMenuAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(page__event__team__in=[request.user,])

    def get_form(self, request, obj=None, **kwargs):
        form = super(EventPageMenuAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['page'].queryset = EventPage.objects.filter(event__team__in=[request.user])
        return form


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
            'fields': ('email', 'password1', 'password2')}
        ),
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
        qs = super(UserAdmin, self).queryset(request)
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
