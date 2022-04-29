from django.contrib.sitemaps import Sitemap

from .models import Story


class BlogSiteMap(Sitemap):
    priority = 0.5

    def items(self):
        return Story.objects.all()

    def location(self, item):
        url = item.post_url
        return url.replace('https://', '')

    def lastmod(self, obj):
        return obj.created

    def _urls(self, page, protocol, domain):
        return super(BlogSiteMap, self)._urls(
            page=page, protocol='https', domain='')
