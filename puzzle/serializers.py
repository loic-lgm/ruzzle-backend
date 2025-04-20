from rest_framework import serializers

from category.models import Category
from category.serializers import CategorySerializer
from brand.models import Brand
from brand.serializers import BrandSerializer
from puzzle.models import Puzzle
from user.serializers import UserSerializer


class PuzzleSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    category = BrandSerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.IntegerField(write_only=True)

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
            "image_url",
            "status",
            "is_published",
            "owner",
        ]

    def create(self, validated_data):
        brand_id = validated_data.pop("brand_id")
        category_id = validated_data.pop("brand_id")
        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            raise serializers.ValidationError({"brand_id": "Marque introuvable."})
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError({"category_id": "Catégorie introuvable."})
        return Puzzle.objects.create(brand=brand, category=category, **validated_data)
