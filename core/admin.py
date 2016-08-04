from datetime import datetime

from django.contrib import admin, messages
from django import forms
from django.forms import ModelForm
from django.contrib.auth import admin as auth_admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import render, redirect

from codemirror import CodeMirrorTextarea
from suit.admin import SortableModelAdmin

from .forms import (
    UserChangeForm, UserCreationForm, UserLimitedChangeForm, AddOrganizerForm
)
from .filters import OpenRegistrationFilter
from .models import (
    Coach, Event, User, EventPage, EventPageContent, EventPageMenu, Postmortem,
    Sponsor, Story
)


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'organizers', 'email', 'date', 'city', 'country',
                    'is_on_homepage', 'is_past_event', 'has_stats')
    list_filter = (OpenRegistrationFilter,)
    search_fields = ('city', 'country', 'name')
    filter_horizontal = ['team']

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

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return ('email', 'team', 'is_deleted', 'is_on_homepage')
        return self.readonly_fields

    def get_urls(self):
        urls = super(EventAdmin, self).get_urls()
        my_urls = [
            url(r'manage_organizers/$',
                self.admin_site.admin_view(self.view_manage_organizers),
                name='core_event_manage_organizers'),
            url(r'add_organizers/$',
                self.admin_site.admin_view(self.view_add_organizers),
                name='core_event_add_organizers'),
        ]
        return my_urls + urls

    def _get_future_events_for_user(self, request):
        """
        Retrieves a list of future events, ordered by name.
        It's based on get_queryset, so superuser see all events, while
        is_staff users see events they're assigned to only.
        """
        return self.get_queryset(request) \
            .filter(date__gte=datetime.now()
                    .strftime("%Y-%m-%d")).order_by('name')

    def _get_event_from_get(self, request, all_events):
        """
        Retrieves a particular event from request.GET['event_id'], or
        returns the first one from all events available to the user.
        """
        if 'event_id' in request.GET:
            try:
                return all_events.get(id=request.GET['event_id'])
            except Event.DoesNotExist:
                pass
        else:
            return all_events.first()

    def view_manage_organizers(self, request):
        """
        Custom admin view that allows user to remove organizers from an event
        """
        all_events = self._get_future_events_for_user(request)
        event = self._get_event_from_get(request, all_events)

        if 'remove' in request.GET and event in all_events:
            user = User.objects.get(id=request.GET['remove'])
            if user in event.team.all():
                event.team.remove(user)
                messages.success(request, 'Organizer {} has been removed'.format(user.get_full_name()))
            return redirect('/admin/core/event/manage_organizers/?event_id={}'.format(event.id))

        return render(request, 'admin/core/event/view_manage_organizers.html', {
            'all_events': all_events,
            'event': event,
        })

    def view_add_organizers(self, request):
        """
        Custom admin view that allows user to add new organizer to an event
        """
        all_events = self._get_future_events_for_user(request)
        event = self._get_event_from_get(request, all_events)

        if request.method == 'POST':
            form = AddOrganizerForm(all_events, request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request,
                    '{} has been added to your event, yay!'.format(user.get_full_name()))
                return redirect('/admin/core/event/manage_organizers/?event_id={}'.format(event.id))
        else:
            form = AddOrganizerForm(all_events)

        return render(request, 'admin/core/event/view_add_organizers.html', {
            'all_events': all_events,
            'event': event,
            'form': form,
        })


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
            else:
                return ('url', 'is_deleted')
        return self.readonly_fields


class ResizableCodeMirror(CodeMirrorTextarea):

    def __init__(self, **kwargs):
        super(ResizableCodeMirror, self).__init__(
            js_var_format='%s_editor', **kwargs)

    @property
    def media(self):
        mine = forms.Media(
            css={'all': ('vendor/jquery-ui/jquery-ui.min.css',)},
            js=('vendor/jquery-ui/jquery-ui.min.js',))
        return super(ResizableCodeMirror, self).media + mine

    def render(self, name, value, attrs=None):
        output = super(ResizableCodeMirror, self).render(name, value, attrs)
        return output + mark_safe(
            '''
                <script type="text/javascript">
                $('.CodeMirror').resizable({
                  resize: function() {
                    %s_editor.setSize($(this).width(), $(this).height());
                  }
                });
                </script>
            ''' % name)


class EventPageContentForm(ModelForm):

    class Meta:
        widgets = {
            'content': ResizableCodeMirror(mode="xml")
        }
        fields = (
            'page',
            'name',
            'content',
            'background',
            'position',
            'is_public',
        )


class SponsorInline(admin.TabularInline):
    model = EventPageContent.sponsors.through
    extra = 1
    verbose_name_plural = 'Sponsors'


class CoachInline(admin.TabularInline):
    model = EventPageContent.coaches.through
    extra = 1
    verbose_name_plural = 'Coaches'


class EventPageContentAdmin(SortableModelAdmin):
    list_display = ('name', 'page', 'position', 'is_public')
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
        form = super(EventPageContentAdmin, self).get_form(
            request, obj, **kwargs)
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


class SponsorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'logo_display_for_admin', 'url')
    list_per_page = 50
    search_fields = ('name', )

    def get_queryset(self, request):
        qs = super(SponsorAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(eventpagecontent__page__event__team=request.user).distinct()

    def get_form(self, request, obj=None, **kwargs):
        form = super(SponsorAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if 'eventpagecontent' in form.base_fields:
                qs = EventPageContent.objects.filter(
                    page__event__team=request.user)
                form.base_fields['eventpagecontent'].queryset = qs
        return form


class CoachAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo_display_for_admin', 'twitter_handle', 'url')
    search_fields = ('name', 'twitter_handle', 'url')

    def get_queryset(self, request):
        qs = super(CoachAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(eventpagecontent__page__event__team=request.user).distinct()

    def get_form(self, request, obj=None, **kwargs):
        form = super(CoachAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if 'eventpagecontent' in form.base_fields:
                qs = EventPageContent.objects.filter(
                    page__event__team=request.user)
                form.base_fields['eventpagecontent'].queryset = qs
        return form


class PostmortemAdmin(admin.ModelAdmin):
    list_display = ('event', 'attendees_count', 'applicants_count')
    raw_id_fields = ('event',)

    def get_changeform_initial_data(self, request):
        initial = super(PostmortemAdmin,
                        self).get_changeform_initial_data(request)
        if "event" in request.GET:
            event = Event.objects.get(pk=request.GET['event'])
            initial['event'] = event
        return initial


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


class StoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_story', 'created')
    search_fields = ('name', 'content')
    list_filter = ('is_story',)


class MyFlatPageAdmin(FlatPageAdmin):

    class MyFlatpageForm(FlatpageForm):
        template_name = forms.CharField(
            initial='flatpage.html',
            help_text="Change this only if you know what you are doing")

    form = MyFlatpageForm

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, MyFlatPageAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventPage, EventPageAdmin)
admin.site.register(EventPageContent, EventPageContentAdmin)
admin.site.register(EventPageMenu, EventPageMenuAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Postmortem, PostmortemAdmin)
admin.site.register(Coach, CoachAdmin)
admin.site.register(Story, StoryAdmin)
