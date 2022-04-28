from django.urls import path
from django.contrib.sitemaps.views import sitemap

from story.views import StoryListView
from story.sitemap import BlogSiteMap

sitemaps = {
    "blog": BlogSiteMap
}

app_name = "story"
urlpatterns = [
    path('', StoryListView.as_view(), name='stories'),
    path('/sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
