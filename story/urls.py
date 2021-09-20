from django.conf.urls import url

from story.views import StoryListView

app_name = "story"
urlpatterns = [
    url(r'^$', StoryListView.as_view(), name='stories'),
]
