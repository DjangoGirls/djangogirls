from django.contrib import admin


class StoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_story', 'created')
    search_fields = ('name', 'content')
    list_filter = ('is_story',)


admin.site.register(Story, StoryAdmin)
