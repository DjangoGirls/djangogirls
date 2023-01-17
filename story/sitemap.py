from django.contrib.sitemaps import Sitemap

from .models import Story


class BlogSiteMap(Sitemap):
    priority = 0.5

    def items(self):
        return Story.objects.all().order_by("-created")

    def location(self, item):
        url = item.post_url
        if url is not None and "http://" in url:
            return url.replace("http://", "")
        else:
            return url.replace("https://", "")

    def lastmod(self, obj):
        return obj.created

    def _urls(self, page, protocol, domain):
        return super()._urls(page=page, protocol="https", domain="")
