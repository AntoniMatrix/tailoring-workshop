"""
Public views + robots.txt content.
"""

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Sum
from django.db.utils import ProgrammingError, OperationalError

def home(request):
    slides = []
    try:
        from orders.models import Order
        latest = list(
            Order.objects
            .prefetch_related("items")
            .annotate(total_qty=Sum("items__qty"))
            .order_by("-created_at")[:10]
        )

        # اسلایدهای واقعی
        slides = [{"kind": "order", "obj": o} for o in latest]

        # اگر کمتر از 10 تا بود، با نمونه پر کن
        missing = 10 - len(slides)
        for i in range(missing):
            slides.append({
                "kind": "sample",
                "id": f"نمونه {i+1}",
                "title": "نمونه سفارش سری‌دوزی",
                "status": "نمونه",
                "qty": 120,
            })

    except (ProgrammingError, OperationalError):
        # DB آماده نیست: کل 10 تا رو نمونه پر کن
        slides = [{
            "kind": "sample",
            "id": f"نمونه {i+1}",
            "title": "نمونه سفارش سری‌دوزی",
            "status": "نمونه",
            "qty": 120,
        } for i in range(10)]

    return render(request, "home.html", {"slides": slides})

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