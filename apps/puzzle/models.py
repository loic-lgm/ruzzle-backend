from django.db import models
from django.utils import timezone

from apps.brand.models import Brand
from apps.category.models import Category
from apps.user.models import User


class Puzzle(models.Model):
    """
    Represents a puzzle.
    """

    CONDITION_CHOICES = [
        ("new", "available"),
        ("used", "used"),
        ("damaged", "damaged"),
    ]

    STATUS_CHOICES = [
        ("available", "available"),
        ("pending", "pending"),
        ("swap", "swap"),
    ]

    name = models.CharField(max_length=255)
    piece_count = models.IntegerField()
    description = models.TextField(max_length=3000)
    condition = models.CharField(choices=CONDITION_CHOICES)
    image = models.ImageField(upload_to="puzzle_images/", blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default="available")
    is_published = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="puzzles", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="puzzles", null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="puzzles")

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name
