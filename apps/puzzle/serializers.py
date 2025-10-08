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
    category_inputs = serializers.ListField(
        child=serializers.JSONField(), write_only=True
    )
    brand = BrandSerializer(read_only=True)
    brand_input = serializers.JSONField(write_only=True)
    hashid = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()

    class Meta:
        model = Puzzle
        fields = [
            "id",
            "name",
            "brand",
            "brand_input",
            "categories",
            "category_inputs",
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

    def get_or_create_items(self, input_data, model, field_name, many=False):
        import json

        items = input_data if many else [input_data]
        results = []
        for item in items:
            if isinstance(item, str):
                try:
                    parsed = json.loads(item)
                    if isinstance(parsed, dict) and parsed.get("isNew") and "name" in parsed:
                        item = parsed
                    else:
                        item = int(item)
                except (json.JSONDecodeError, ValueError):
                    raise serializers.ValidationError(
                        {field_name: f"Format invalide pour {item}."}
                    )
            if isinstance(item, int):
                try:
                    obj = model.objects.get(id=item)
                except model.DoesNotExist:
                    raise serializers.ValidationError(
                        {field_name: f"{model.__name__} {item} introuvable."}
                    )
                results.append(obj)
                continue
            if isinstance(item, dict) and item.get("isNew") and "name" in item:
                name = item["name"].strip().capitalize()
                obj, _ = model.objects.get_or_create(name=name)
                results.append(obj)
                continue
            raise serializers.ValidationError(
                {field_name: f"Format invalide pour {item}."}
            )
        return results if many else results[0]

    def validate(self, attrs):
        categories = attrs.get("category_inputs", [])
        if not (1 <= len(categories) <= 3):
            raise serializers.ValidationError(
                {
                    "error": "Tu dois sélectionner entre 1 et 3 catégories pour ton puzzle."
                }
            )
        return attrs

    def validate_image(self, value):
        try:
            return validate_image(value)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def create(self, validated_data):
        brand_input = validated_data.pop("brand_input")
        category_inputs = validated_data.pop("category_inputs")
        categories = self.get_or_create_items(
            input_data=category_inputs,
            model=Category,
            field_name="category_inputs",
            many=True,
        )
        brand = self.get_or_create_items(brand_input, Brand, "brand_input")
        puzzle = Puzzle.objects.create(brand=brand, **validated_data)
        puzzle.categories.set(categories)
        return puzzle

    def update(self, instance, validated_data):
        if "image" in validated_data and instance.image:
            instance.image.delete(save=False)
        if "category_inputs" in validated_data:
            category_inputs = validated_data.pop("category_inputs")
            categories = self.get_or_create_items(
                input_data=category_inputs,
                model=Category,
                field_name="category_inputs",
                many=True,
            )
            instance.categories.set(categories)
        if "brand_input" in validated_data:
            brand_input = validated_data.pop("brand_input")
            instance.brand = self.get_or_create_items(brand_input, Brand, "brand_input")
        return super().update(instance, validated_data)
