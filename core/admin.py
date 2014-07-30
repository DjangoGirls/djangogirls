from django.contrib import admin

from .models import *

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'city', 'country')

class EventPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'is_live')

class EventPageContentAdmin(admin.ModelAdmin):
    list_display = ('name', 'page', 'content', 'position', 'is_public')

class EventPageMenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'page', 'url', 'position')

admin.site.register(Event, EventAdmin)
admin.site.register(EventPage, EventPageAdmin)
admin.site.register(EventPageContent, EventPageContentAdmin)
admin.site.register(EventPageMenu, EventPageMenuAdmin)
