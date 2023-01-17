from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
    def items(self):
        return [
            "core:index",
            "core:foundation",
            "core:foundation-governing-document",
            "core:contribute",
            "core:year_2015",
            "core:year_2016_2017",
            "core:events",
            "core:newsletter",
            "core:resources",
            "donations:index",
            "organize:index",
        ]

    def location(self, item):
        return reverse(item)
