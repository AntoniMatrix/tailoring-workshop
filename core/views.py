"""
Public views + robots.txt content.
"""

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    """Public landing page."""
    return render(request, "home.html")


def robots_txt(request):
    """
    Robots policy:
    - Allow public crawling
    - Disallow private/auth/panel/api routes
    - Provide sitemap location
    """
    site_url = getattr(settings, "SITE_URL", "").rstrip("/")
    sitemap_url = f"{site_url}/sitemap.xml" if site_url else "/sitemap.xml"

    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /panel/",
        "Disallow: /accounts/",
        "Disallow: /orders/",
        "Disallow: /api/",
        "",
        f"Sitemap: {sitemap_url}",
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")