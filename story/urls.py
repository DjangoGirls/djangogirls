from django.conf.urls import url

from story.views import StoryListView

urlpatterns = [
    url(r'^$', StoryListView.as_view(), name='stories'),
]
