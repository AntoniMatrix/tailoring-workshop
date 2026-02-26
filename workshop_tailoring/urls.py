"""
Root URL routing:
- Public pages (core)
- Auth (accounts)
- Customer pages (orders)
- Staff panel (adminpanel)
- APIs (orders)
- SEO: robots.txt + sitemap.xml
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("orders/", include("orders.urls")),
    path("panel/", include("adminpanel.urls")),

    path("api/orders/", include("orders.api_urls")),

    # SEO endpoints
    path("sitemap.xml", sitemap, {"sitemaps": {"static": StaticViewSitemap}}, name="sitemap"),
    path("robots.txt", include("core.urls_robots")),  # dedicated urls module for robots
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)