from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Order


@login_required
def customer_orders_page(request):
    """Customer orders list page (JS will fetch data)."""
    return render(request, "customer/orders.html")


@login_required
def customer_order_detail_page(request, order_id: int):
    """Customer order detail page (owner only)."""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, "customer/order_detail.html", {"order": order})