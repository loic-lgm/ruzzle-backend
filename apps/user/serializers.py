from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.city.serializers import CitySerializer


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
            'latitude',
            'longitude',
            'postal_code',
            'city_name',
            "created_at",
            "rating",
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
            "city_name",
            "postal_code",
            "puzzles",
            "created_at",
        ]

    def get_puzzles(self, obj):
        from apps.puzzle.serializers import PuzzleSerializer

        puzzles = obj.puzzles.exclude(status__in=["swapped", "deleted"])
        return PuzzleSerializer(puzzles, many=True, context=self.context).data
