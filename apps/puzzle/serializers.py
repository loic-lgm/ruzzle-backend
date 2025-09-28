from rest_framework import serializers

from apps.category.models import Category
from apps.brand.models import Brand
from apps.brand.serializers import BrandSerializer
from apps.puzzle.models import Puzzle
from apps.user.serializers import UserSerializer
from apps.utils.validations import validate_image


class PuzzleSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    category = BrandSerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.IntegerField(write_only=True)
    hashid = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()

    class Meta:
        model = Puzzle
        fields = [
            "id",
            "name",
            "brand",
            "brand_id",
            "category",
            "category_id",
            "piece_count",
            "description",
            "condition",
            "image",
            "status",
            "is_published",
            "width",
            "height",
            "owner",
            "hashid",
            "created",
        ]

    def validate_image(self, value):
        return validate_image(value, serializers=self)

    def create(self, validated_data):
        brand_id = validated_data.pop("brand_id")
        category_id = validated_data.pop("category_id")
        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            raise serializers.ValidationError({"brand_id": "Marque introuvable."})
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError({"category_id": "Catégorie introuvable."})
        return Puzzle.objects.create(brand=brand, category=category, **validated_data)

    def update(self, instance, validated_data):
        if "image" in validated_data and instance.image:
            instance.image.delete(save=False)
        return super().update(instance, validated_data)
