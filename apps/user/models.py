from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

from apps.city.models import City


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crée et renvoie un superutilisateur avec un email.
        """
        if not email:
            raise ValueError('Le superutilisateur doit avoir un email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    Represents a customer user.
    """

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    image = models.ImageField(upload_to="user_images/", blank=True, null=True, max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    city = models.ForeignKey(
        City, on_delete=models.PROTECT, related_name="users", null=True, blank=True
    )

    objects = CustomUserManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
