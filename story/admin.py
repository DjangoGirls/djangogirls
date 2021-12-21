from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from .models import Story
from .services import (
    create_missing_stories,
    request_latest_stories_from_tumblr,
)


def load_remote_stories(modeladmin, request, queryset):
    latest_stories = request_latest_stories_from_tumblr()
    create_missing_stories(list(latest_stories))


load_remote_stories.short_description = _("Load remote stories")


class StoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_story', 'created')
    search_fields = ('name', 'content')
    list_filter = ('is_story',)
    actions = [
        load_remote_stories,
    ]


admin.site.register(Story, StoryAdmin)
