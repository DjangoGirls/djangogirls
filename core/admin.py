from datetime import datetime

from codemirror import CodeMirrorTextarea
from django import forms
from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.auth import admin as auth_admin
from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from suit.admin import SortableModelAdmin

from .filters import OpenRegistrationFilter
from .forms import (AddOrganizerForm, UserChangeForm, UserCreationForm,
                    UserLimitedChangeForm)
from .models import (Coach, Event, EventPageContent, EventPageMenu,
                     Postmortem, Sponsor, Story, User)


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'organizers', 'email', 'date', 'city', 'country',
                    'is_on_homepage', 'is_past_event', 'has_stats')
    list_filter = (OpenRegistrationFilter,)
    search_fields = ('city', 'country', 'name')
    filter_horizontal = ['team']

    def get_queryset(self, request):
        qs = super(EventAdmin, self).get_queryset(request)
        qs = qs.annotate(postmortem_count=Count('postmortem'))
        qs = qs.prefetch_related('team')
        if request.user.is_superuser:
            return qs
        return qs.filter(team=request.user)

    def is_past_event(self, obj):
        return not obj.is_upcoming()
    is_past_event.boolean = True
    is_past_event.short_description = 'past event?'

    def has_stats(self, obj):
        return obj.postmortem_count > 0
    has_stats.boolean = True
    has_stats.short_description = 'has stats?'

    def full_url(self, obj):
        url = reverse('core:event', kwargs={'city': obj.page_url})
        url = 'https://djangogirls.org{url}'.format(url=url)
        return mark_safe('<a href="{url}">{url}</a>'.format(url=url))
    full_url.short_description = 'page URL'

    def get_readonly_fields(self, request, obj=None):
        fields = set(self.readonly_fields) | {'full_url'}
        if obj and not request.user.is_superuser:
            fields.update({
                'city', 'country', 'date', 'email', 'is_on_homepage', 'name',
                'page_url', 'team'})
            # Don't let change objects for events that already happened
            if not obj.is_upcoming():
                fields.update({x.name for x in self.model._meta.fields})
        return fields

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return [
                ('Event info', {'fields': [
                    'name',
                    'date',
                    'city',
                    'country',
                    'latlng',
                    'email',
                    'page_url',
                    'is_deleted'
                ]}),
                ('Home page', {'fields': [
                    'photo',
                    'photo_credit',
                    'photo_link',
                    'is_on_homepage'
                ]}),
                ('Team', {'fields': [
                    'main_organizer',
                    'team'
                ]}),
                ('Event page', {'fields': [
                    'page_title',
                    'page_description',
                    'page_main_color',
                    'page_custom_css',
                    'is_page_live'
                ]})
            ]
        return [
            ('Event info', {'fields': [
                'name',
                'date',
                'city',
                'country',
                'full_url'
            ]}),
            ('Home page', {'fields': [
                'photo',
                'photo_credit',
                'photo_link',
            ]}),
            ('Event page', {'fields': [
                'page_title',
                'page_description',
                'page_main_color',
                'page_custom_css',
                'is_page_live'
            ]})
        ]


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
            if user == request.user:
                messages.error(request, 'You cannot remove yourself from a team.')
            else:
                if user in event.team.all():
                    event.team.remove(user)
                    messages.success(request, 'Organizer {} has been removed'.format(user.get_full_name()))
                    return HttpResponseRedirect(
                        reverse('admin:core_event_manage_organizers') + '?event_id={}'.format(event.id))

        return render(request, 'admin/core/event/view_manage_organizers.html', {
            'all_events': all_events,
            'event': event,
            'title': 'Remove organizers',
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
                    "{} has been added to your event, yay! They've been also" \
                    " invited to Slack and should receive credentials to login" \
                    " in an e-mail.".format(user.get_full_name()))
                return redirect('admin:core_event_add_organizers')
        else:
            form = AddOrganizerForm(all_events)

        return render(request, 'admin/core/event/view_add_organizers.html', {
            'all_events': all_events,
            'event': event,
            'form': form,
            'title': 'Add organizers',
        })


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
            'event',
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
    list_display = ('name', 'event', 'position', 'is_public')
    list_filter = ('event', 'is_public')
    search_fields = ('name', 'event__page_title', 'content', 'event__city',
                     'event__country', 'event__name')
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
        return qs.filter(event__team=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super(EventPageContentAdmin, self).get_form(
            request, obj, **kwargs)
        if not request.user.is_superuser:
            if 'event' in form.base_fields:
                form.base_fields['event'].queryset = Event.objects.filter(
                    team=request.user
                )
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            # Don't let change objects for events that already happened
            if not obj.event.is_upcoming():
                return set([x.name for x in self.model._meta.fields])
        return self.readonly_fields


class EventPageMenuAdmin(SortableModelAdmin):
    list_display = ('title', 'event', 'url', 'position')
    list_filter = ('event',)
    sortable = 'position'

    def get_queryset(self, request):
        qs = super(EventPageMenuAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(event__team=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super(EventPageMenuAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if 'event' in form.base_fields:
                form.base_fields['event'].queryset = Event.objects.filter(
                    team=request.user
                )
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            # Don't let change objects for events that already happened
            if not obj.event.is_upcoming():
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
        return qs.filter(eventpagecontent__event__team=request.user).distinct()

    def get_form(self, request, obj=None, **kwargs):
        form = super(SponsorAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if 'eventpagecontent' in form.base_fields:
                qs = EventPageContent.objects.filter(
                    event__team=request.user)
                form.base_fields['eventpagecontent'].queryset = qs
        return form


class CoachAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo_display_for_admin', 'twitter_handle', 'url')
    search_fields = ('name', 'twitter_handle', 'url')

    def get_queryset(self, request):
        qs = super(CoachAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(eventpagecontent__event__team=request.user).distinct()

    def get_form(self, request, obj=None, **kwargs):
        form = super(CoachAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if 'eventpagecontent' in form.base_fields:
                qs = EventPageContent.objects.filter(
                    event__team=request.user)
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
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'date_joined')
    list_filter = ('event', 'is_staff', 'is_superuser', 'is_active', 'groups', 'date_joined')
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
admin.site.register(EventPageContent, EventPageContentAdmin)
admin.site.register(EventPageMenu, EventPageMenuAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Postmortem, PostmortemAdmin)
admin.site.register(Coach, CoachAdmin)
admin.site.register(Story, StoryAdmin)
