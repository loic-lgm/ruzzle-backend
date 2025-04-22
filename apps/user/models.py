from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

from apps.city.models import City


class User(AbstractUser):
    """
    Represents a customer user.
    """

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    image = models.URLField(blank=True, null=True, max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    city = models.ForeignKey(
        City, on_delete=models.PROTECT, related_name="users", null=True, blank=True
    )


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
