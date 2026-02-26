from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Expose custom fields in Django Admin."""
    fieldsets = UserAdmin.fieldsets + (("Extra", {"fields": ("phone",)}),)