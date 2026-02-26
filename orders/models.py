"""
Order domain models.

Security considerations:
- Internal notes (OrderMessage.is_internal=True) never shown to customers.
- File uploads should be validated by extension/size (validators.py).
"""

from django.conf import settings
from django.db import models
from .validators import validate_upload


class OrderStatus(models.TextChoices):
    """Order lifecycle."""
    NEW = "new", "جدید"
    REVIEW = "review", "در حال بررسی"
    QUOTED = "quoted", "پیش‌فاکتور صادر شد"
    CONFIRMED = "confirmed", "تأیید شد"
    PRODUCTION = "production", "در حال تولید"
    READY = "ready", "آماده تحویل"
    DELIVERED = "delivered", "تحویل شد"
    CANCELED = "canceled", "لغو شد"


class Order(models.Model):
    """Order header."""
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    title = models.CharField(max_length=150)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.NEW)

    deadline_date = models.DateField(null=True, blank=True)
    total_price = models.PositiveIntegerField(default=0)
    deposit_amount = models.PositiveIntegerField(default=0)

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_orders",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.title}"


class OrderItem(models.Model):
    """Line item."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_type = models.CharField(max_length=80)
    qty = models.PositiveIntegerField(default=1)
    size_range = models.CharField(max_length=120, blank=True)
    fabric_type = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)


class OrderFile(models.Model):
    """Attachments (validated)."""
    class FileType(models.TextChoices):
        PATTERN = "pattern", "الگو"
        SAMPLE = "sample", "نمونه"
        REFERENCE = "reference", "مرجع"
        INVOICE = "invoice", "فاکتور"
        OTHER = "other", "سایر"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="files")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to="orders/files/", validators=[validate_upload])
    type = models.CharField(max_length=20, choices=FileType.choices, default=FileType.OTHER)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderMessage(models.Model):
    """Order thread messages; internal notes are staff-only."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    is_internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    """Payment entries (manual for MVP)."""
    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "در انتظار"
        PAID = "paid", "پرداخت شده"
        FAILED = "failed", "ناموفق"
        REFUNDED = "refunded", "برگشت خورده"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    amount = models.PositiveIntegerField()
    method = models.CharField(max_length=30, default="card")
    status = models.CharField(max_length=15, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    ref_code = models.CharField(max_length=80, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)