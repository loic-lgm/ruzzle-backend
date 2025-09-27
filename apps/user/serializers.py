from multiprocessing import context
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.city.models import City
from apps.city.serializers import CitySerializer
from apps.utils.validations import validate_image


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "image",
            "city",
            "created_at",
        ]

    def validate_username(self, value):
        if " " in value:
            raise serializers.ValidationError(
                {"error": "Le nom d'utilisateur ne peut pas contenir d'espaces."}
            )
        return value

class UserPublicSerializer(UserSerializer):
    puzzles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "image",
            "city",
            "puzzles",
            "created_at",
        ]

    def get_puzzles(self, obj):
        from apps.puzzle.serializers import PuzzleSerializer

        puzzles = obj.puzzles.exclude(status__in=["swapped", "deleted"])
        return PuzzleSerializer(puzzles, many=True, context=self.context).data
