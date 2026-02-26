"""
RBAC helpers:
- staff role = belongs to at least one group OR superuser
- permissions = standard Django permissions + custom perms (seeded)
"""


def is_staff_role(user) -> bool:
    """Return True if user is staff (role/group based) or superuser."""
    return bool(user.is_authenticated and (user.is_superuser or user.groups.exists()))


def has_perm(user, perm_codename: str) -> bool:
    """Check a custom permission in the 'orders' app namespace."""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.has_perm(f"orders.{perm_codename}")