from django.contrib.sitemaps import Sitemap

from .models import Story


class BlogSiteMap(Sitemap):
    priority = 0.5

    def items(self):
        return Story.objects.all()

    def lastmod(self, obj):
        return obj.created
