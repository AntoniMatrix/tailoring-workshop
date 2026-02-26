"""
Create default staff roles (Groups) + custom permissions.

Usage:
    python manage.py seed_roles
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from orders.models import Order


class Command(BaseCommand):
    help = "Seed roles and permissions for RBAC"

    def handle(self, *args, **kwargs):
        ct = ContentType.objects.get_for_model(Order)

        custom = {
            "view_all_orders": "Can view all orders",
            "change_order_status": "Can change order status",
            "set_pricing": "Can set pricing",
            "view_financial_reports": "Can view financial reports",
        }

        perm_objs = {}
        for code, name in custom.items():
            perm, _ = Permission.objects.get_or_create(
                codename=code,
                name=name,
                content_type=ct,
            )
            perm_objs[code] = perm

        roles = {
            "Workshop Manager": ["view_all_orders", "change_order_status", "set_pricing", "view_financial_reports"],
            "Order Operator": ["view_all_orders", "change_order_status"],
            "Accountant": ["view_all_orders", "view_financial_reports"],
            "Production": ["view_all_orders", "change_order_status"],
        }

        for role, codes in roles.items():
            group, _ = Group.objects.get_or_create(name=role)
            group.permissions.clear()
            for c in codes:
                group.permissions.add(perm_objs[c])

        self.stdout.write(self.style.SUCCESS("✅ Roles seeded successfully."))