from django.contrib import admin
from .models import Order, OrderItem, OrderFile, OrderMessage, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderFileInline(admin.TabularInline):
    model = OrderFile
    extra = 0


class OrderMessageInline(admin.TabularInline):
    model = OrderMessage
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin list for quick triage."""
    list_display = ("id", "title", "customer", "status", "total_price", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "customer__username", "customer__email")
    inlines = [OrderItemInline, OrderFileInline, OrderMessageInline]


admin.site.register(Payment)