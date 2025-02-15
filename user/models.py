from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Represents a customer user.
    """

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    image = models.URLField(blank=True, null=True, max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
