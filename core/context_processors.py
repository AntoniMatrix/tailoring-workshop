"""
SEO context processor:
injects site defaults + current absolute URL for canonical tags.
"""

from django.conf import settings


def seo_defaults(request):
    """Return global SEO variables for templates."""
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "Website"),
        "SITE_URL": getattr(settings, "SITE_URL", "").rstrip("/"),
        "SITE_DEFAULT_DESCRIPTION": getattr(settings, "SITE_DEFAULT_DESCRIPTION", ""),
        "SITE_DEFAULT_OG_IMAGE": getattr(settings, "SITE_DEFAULT_OG_IMAGE", ""),
        "BUSINESS": getattr(settings, "BUSINESS", {}),
        "CURRENT_URL": request.build_absolute_uri(),
    }