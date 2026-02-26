"""
Sitemap config (public, indexable pages only).
Private pages (accounts/panel/orders details) should be noindex and excluded.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Sitemap for public pages."""
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["home"]

    def location(self, item):
        return reverse(item)