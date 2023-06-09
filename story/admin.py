from django.contrib import admin

from story.models import Story


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_story", "created")
    search_fields = ("name", "content")
    list_filter = ("is_story",)
