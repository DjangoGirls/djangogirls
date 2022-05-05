from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from .models import Story


class StoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_story', 'created')
    search_fields = ('name', 'content')
    list_filter = ('is_story',)


admin.site.register(Story, StoryAdmin)
