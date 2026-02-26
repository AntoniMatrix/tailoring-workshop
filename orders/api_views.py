"""
JSON endpoints consumed by Vanilla JS.

Security:
- Customer endpoints always scope by request.user
- Staff endpoints require staff role AND specific permissions
- Rate limiting on write endpoints to reduce spam/abuse
"""

import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_ratelimit.decorators import ratelimit

from .models import Order, OrderItem, OrderMessage, Payment, OrderStatus
from .permissions import is_staff_role, has_perm


def _bad(msg: str, code: int = 400) -> JsonResponse:
    """Standard JSON error response."""
    return JsonResponse({"ok": False, "error": msg}, status=code)


# -----------------------
# Customer APIs
# -----------------------

@login_required
@require_http_methods(["GET"])
def my_orders(request):
    """List current user's orders."""
    qs = Order.objects.filter(customer=request.user).order_by("-created_at")
    return JsonResponse(
        {
            "ok": True,
            "orders": [
                {
                    "id": o.id,
                    "title": o.title,
                    "status": o.status,
                    "status_label": o.get_status_display(),
                    "total_price": o.total_price,
                    "deposit_amount": o.deposit_amount,
                    "created_at": o.created_at.isoformat(),
                }
                for o in qs
            ],
        }
    )


@login_required
@ratelimit(key="user_or_ip", rate="20/m", block=True)
@require_http_methods(["POST"])
def create_order(request):
    """Create a new order and its items."""
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return _bad("Invalid JSON payload.")

    title = (payload.get("title") or "").strip()
    items = payload.get("items") or []

    if not title:
        return _bad("title required")
    if len(title) > 150:
        return _bad("title too long")

    order = Order.objects.create(customer=request.user, title=title)

    for it in items:
        qty = int(it.get("qty") or 1)
        if qty <= 0 or qty > 100000:
            return _bad("Invalid qty")

        OrderItem.objects.create(
            order=order,
            product_type=(it.get("product_type") or "").strip()[:80],
            qty=qty,
            size_range=(it.get("size_range") or "").strip()[:120],
            fabric_type=(it.get("fabric_type") or "").strip()[:120],
            notes=(it.get("notes") or "").strip(),
        )

    return JsonResponse({"ok": True, "order_id": order.id})


@login_required
@require_http_methods(["GET"])
def my_order_detail(request, order_id: int):
    """Get order details for owner only; hide internal messages."""
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    return JsonResponse(
        {
            "ok": True,
            "order": {
                "id": order.id,
                "title": order.title,
                "status": order.status,
                "status_label": order.get_status_display(),
                "total_price": order.total_price,
                "deposit_amount": order.deposit_amount,
                "created_at": order.created_at.isoformat(),
            },
            "items": [
                {
                    "id": i.id,
                    "product_type": i.product_type,
                    "qty": i.qty,
                    "size_range": i.size_range,
                    "fabric_type": i.fabric_type,
                    "notes": i.notes,
                }
                for i in order.items.all()
            ],
            "messages": [
                {
                    "id": m.id,
                    "sender": getattr(m.sender, "username", "unknown"),
                    "message": m.message,
                    "created_at": m.created_at.isoformat(),
                }
                for m in order.messages.filter(is_internal=False).order_by("created_at")
            ],
            "payments": [
                {
                    "id": p.id,
                    "amount": p.amount,
                    "method": p.method,
                    "status": p.status,
                    "status_label": p.get_status_display(),
                    "created_at": p.created_at.isoformat(),
                }
                for p in order.payments.order_by("-created_at")
            ],
        }
    )


@login_required
@ratelimit(key="user_or_ip", rate="30/m", block=True)
@require_http_methods(["POST"])
def add_message_customer(request, order_id: int):
    """Add a customer message to their order thread."""
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return _bad("Invalid JSON payload.")

    text = (payload.get("message") or "").strip()
    if not text:
        return _bad("Message cannot be empty.")
    if len(text) > 5000:
        return _bad("Message too long.")

    OrderMessage.objects.create(order=order, sender=request.user, message=text, is_internal=False)
    return JsonResponse({"ok": True})


# -----------------------
# Staff APIs
# -----------------------

def _require_staff_perm(request, codename: str):
    """Centralized staff role + permission check."""
    if not is_staff_role(request.user):
        return _bad("Forbidden", 403)
    if not has_perm(request.user, codename):
        return _bad("No permission", 403)
    return None


@login_required
@require_http_methods(["GET"])
def staff_orders(request):
    """List all orders (requires view_all_orders)."""
    err = _require_staff_perm(request, "view_all_orders")
    if err:
        return err

    qs = Order.objects.all().order_by("-created_at")
    return JsonResponse(
        {
            "ok": True,
            "orders": [
                {
                    "id": o.id,
                    "title": o.title,
                    "customer": o.customer.username,
                    "status": o.status,
                    "status_label": o.get_status_display(),
                    "total_price": o.total_price,
                    "deposit_amount": o.deposit_amount,
                    "created_at": o.created_at.isoformat(),
                }
                for o in qs
            ],
        }
    )


@login_required
@require_http_methods(["GET"])
def staff_order_detail(request, order_id: int):
    """Order detail for staff (includes internal messages)."""
    err = _require_staff_perm(request, "view_all_orders")
    if err:
        return err

    order = get_object_or_404(Order, id=order_id)

    return JsonResponse(
        {
            "ok": True,
            "order": {
                "id": order.id,
                "title": order.title,
                "customer": order.customer.username,
                "status": order.status,
                "status_label": order.get_status_display(),
                "total_price": order.total_price,
                "deposit_amount": order.deposit_amount,
                "created_at": order.created_at.isoformat(),
            },
            "items": [
                {
                    "id": i.id,
                    "product_type": i.product_type,
                    "qty": i.qty,
                    "size_range": i.size_range,
                    "fabric_type": i.fabric_type,
                    "notes": i.notes,
                }
                for i in order.items.all()
            ],
            "messages": [
                {
                    "id": m.id,
                    "sender": getattr(m.sender, "username", "unknown"),
                    "message": m.message,
                    "is_internal": m.is_internal,
                    "created_at": m.created_at.isoformat(),
                }
                for m in order.messages.order_by("created_at")
            ],
            "payments": [
                {
                    "id": p.id,
                    "amount": p.amount,
                    "method": p.method,
                    "status": p.status,
                    "status_label": p.get_status_display(),
                    "created_at": p.created_at.isoformat(),
                }
                for p in order.payments.order_by("-created_at")
            ],
            "can_set_pricing": has_perm(request.user, "set_pricing"),
            "can_change_status": has_perm(request.user, "change_order_status"),
            "can_view_financial": has_perm(request.user, "view_financial_reports"),
        }
    )


@login_required
@ratelimit(key="user_or_ip", rate="60/m", block=True)
@require_http_methods(["POST"])
def staff_set_pricing(request, order_id: int):
    """Set order pricing (requires set_pricing)."""
    err = _require_staff_perm(request, "set_pricing")
    if err:
        return err

    order = get_object_or_404(Order, id=order_id)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return _bad("Invalid JSON payload.")

    total = int(payload.get("total_price") or 0)
    deposit = int(payload.get("deposit_amount") or 0)
    if total < 0 or deposit < 0:
        return _bad("Invalid price values.")

    order.total_price = total
    order.deposit_amount = deposit
    order.save(update_fields=["total_price", "deposit_amount", "updated_at"])
    return JsonResponse({"ok": True})


@login_required
@ratelimit(key="user_or_ip", rate="60/m", block=True)
@require_http_methods(["POST"])
def staff_change_status(request, order_id: int):
    """Change order status (requires change_order_status)."""
    err = _require_staff_perm(request, "change_order_status")
    if err:
        return err

    order = get_object_or_404(Order, id=order_id)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return _bad("Invalid JSON payload.")

    status = (payload.get("status") or "").strip()
    valid = {s[0] for s in OrderStatus.choices}
    if status not in valid:
        return _bad("Invalid status.")

    order.status = status
    order.save(update_fields=["status", "updated_at"])

    # Audit trail as internal note
    OrderMessage.objects.create(
        order=order,
        sender=request.user,
        message=f"Status changed to: {order.get_status_display()}",
        is_internal=True,
    )
    return JsonResponse({"ok": True})


@login_required
@ratelimit(key="user_or_ip", rate="60/m", block=True)
@require_http_methods(["POST"])
def staff_add_internal_note(request, order_id: int):
    """Add internal staff note (requires view_all_orders)."""
    err = _require_staff_perm(request, "view_all_orders")
    if err:
        return err

    order = get_object_or_404(Order, id=order_id)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return _bad("Invalid JSON payload.")

    text = (payload.get("message") or "").strip()
    if not text:
        return _bad("Note cannot be empty.")
    if len(text) > 5000:
        return _bad("Note too long.")

    OrderMessage.objects.create(order=order, sender=request.user, message=text, is_internal=True)
    return JsonResponse({"ok": True})


@login_required
@ratelimit(key="user_or_ip", rate="60/m", block=True)
@require_http_methods(["POST"])
def staff_add_payment(request, order_id: int):
    """Add payment (requires view_financial_reports)."""
    err = _require_staff_perm(request, "view_financial_reports")
    if err:
        return err

    order = get_object_or_404(Order, id=order_id)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return _bad("Invalid JSON payload.")

    amount = int(payload.get("amount") or 0)
    method = (payload.get("method") or "card").strip()[:30]
    status = (payload.get("status") or "paid").strip()

    if amount <= 0:
        return _bad("Amount must be > 0.")

    payment = Payment.objects.create(
        order=order,
        amount=amount,
        method=method,
        status=status,
        paid_at=timezone.now() if status == "paid" else None,
    )
    return JsonResponse({"ok": True, "payment_id": payment.id})