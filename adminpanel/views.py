"""
Staff panel HTML pages.
Authorization:
- must be staff (group/superuser)
- must have minimum required perms for pages
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

from orders.models import Order, OrderStatus
from orders.permissions import is_staff_role, has_perm


@login_required
def dashboard(request):
    """Dashboard page for staff."""
    if not is_staff_role(request.user):
        return HttpResponseForbidden("Forbidden")

    stats = {
        "new": Order.objects.filter(status=OrderStatus.NEW).count(),
        "review": Order.objects.filter(status=OrderStatus.REVIEW).count(),
        "quoted": Order.objects.filter(status=OrderStatus.QUOTED).count(),
        "confirmed": Order.objects.filter(status=OrderStatus.CONFIRMED).count(),
        "production": Order.objects.filter(status=OrderStatus.PRODUCTION).count(),
        "ready": Order.objects.filter(status=OrderStatus.READY).count(),
    }
    perms = {
        "view_all_orders": has_perm(request.user, "view_all_orders"),
        "change_order_status": has_perm(request.user, "change_order_status"),
        "set_pricing": has_perm(request.user, "set_pricing"),
        "view_financial_reports": has_perm(request.user, "view_financial_reports"),
    }
    return render(request, "adminpanel/dashboard.html", {"stats": stats, "perms": perms})


@login_required
def orders_page(request):
    """Orders list page (requires view_all_orders)."""
    if not is_staff_role(request.user):
        return HttpResponseForbidden("Forbidden")
    if not has_perm(request.user, "view_all_orders"):
        return HttpResponseForbidden("No permission")
    return render(request, "adminpanel/orders.html")


@login_required
def order_detail_page(request, order_id: int):
    """Order detail management page (requires view_all_orders)."""
    if not is_staff_role(request.user):
        return HttpResponseForbidden("Forbidden")
    if not has_perm(request.user, "view_all_orders"):
        return HttpResponseForbidden("No permission")
    return render(request, "adminpanel/order_detail.html", {"order_id": order_id})