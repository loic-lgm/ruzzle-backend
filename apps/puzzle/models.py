from ast import Try
from django.db import models
from django.utils import timezone

from apps.brand.models import Brand
from apps.category.models import Category
from apps.user.models import User

from hashids import Hashids

hashids = Hashids(min_length=6, salt="ruzzlepuzzle")


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
        ("swapped", "swapped"),
        ("deleted", "deleted"),
    ]

    name = models.CharField(max_length=255, blank=True, null=True)
    piece_count = models.IntegerField()
    description = models.TextField(max_length=3000, blank=True, null=True)
    condition = models.CharField(choices=CONDITION_CHOICES)
    image = models.ImageField(upload_to="puzzle_images/", blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default="available")
    is_published = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, related_name="puzzles", null=True, blank=True
    )
    categories = models.ManyToManyField(Category, related_name="puzzles")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="puzzles")

    @property
    def hashid(self):
        return hashids.encode(self.id)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return str(self.id)
