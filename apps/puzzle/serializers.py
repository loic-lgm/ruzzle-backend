from rest_framework import serializers

from apps.category.models import Category
from apps.brand.models import Brand
from apps.brand.serializers import BrandSerializer
from apps.category.serializers import CategorySerializer
from apps.puzzle.models import Puzzle
from apps.user.serializers import UserSerializer
from apps.utils.validations import validate_image


class PuzzleSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    categories = CategorySerializer(read_only=True, many=True)
    category_ids = serializers.ListField(child=serializers.JSONField(), write_only=True)
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
            "categories",
            "category_ids",
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

    def _get_or_create_categories(self, category_inputs):
        import json

        categories = []
        for item in category_inputs:
            if isinstance(item, str):
                try:
                    parsed = json.loads(item)
                    if (
                        isinstance(parsed, dict)
                        and parsed.get("isNew")
                        and "name" in parsed
                    ):
                        item = parsed
                    else:
                        item = int(item)
                except json.JSONDecodeError:
                    try:
                        item = int(item)
                    except ValueError:
                        raise serializers.ValidationError(
                            {"category_ids": f"Format invalide pour {item}."}
                        )

            if isinstance(item, int):
                try:
                    cat = Category.objects.get(id=item)
                except Category.DoesNotExist:
                    raise serializers.ValidationError(
                        {"category_ids": f"Catégorie {item} introuvable."}
                    )
                categories.append(cat)
            elif isinstance(item, dict) and item.get("isNew") and "name" in item:
                name = item["name"].strip().capitalize()  # première lettre en majuscule
                category, _ = Category.objects.get_or_create(name=name)
                categories.append(category)

            else:
                raise serializers.ValidationError(
                    {"category_ids": f"Format invalide pour {item}."}
                )

        return categories

    def validate(self, attrs):
        categories = attrs.get("category_ids", [])
        if not (1 <= len(categories) <= 3):
            raise serializers.ValidationError(
                {
                    "error": "Tu dois sélectionner entre 1 et 3 catégories pour ton puzzle."
                }
            )
        return attrs

    def validate_image(self, value):
        return validate_image(value, serializers=self)

    def create(self, validated_data):
        brand_id = validated_data.pop("brand_id")
        category_inputs = validated_data.pop("category_ids")
        categories = self._get_or_create_categories(category_inputs)
        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            raise serializers.ValidationError({"brand_id": "Marque introuvable."})
        puzzle = Puzzle.objects.create(brand=brand, **validated_data)
        puzzle.categories.set(categories)
        return puzzle

    def update(self, instance, validated_data):
        if "image" in validated_data and instance.image:
            instance.image.delete(save=False)
        if "category_ids" in validated_data:
            category_inputs = validated_data.pop("category_ids")
            categories = self._get_or_create_categories(category_inputs)
            instance.categories.set(categories)
        return super().update(instance, validated_data)
