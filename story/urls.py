from django.urls import path

from story.views import StoryListView

app_name = "story"
urlpatterns = [
    path("", StoryListView.as_view(), name="stories"),
]
