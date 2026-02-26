"""
Custom user model.

We use AbstractUser and manage roles via Django Groups + Permissions.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User with optional phone field."""
    phone = models.CharField(max_length=20, blank=True)