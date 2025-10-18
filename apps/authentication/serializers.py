from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.city.models import City

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(write_only=True, required=False)
    postal_code = serializers.CharField(write_only=True, required=False)
    latitude = serializers.DecimalField(
        max_digits=9, decimal_places=6, write_only=True, required=False
    )
    longitude = serializers.DecimalField(
        max_digits=9, decimal_places=6, write_only=True, required=False
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "image",
            "city_name",
            "postal_code",
            "latitude",
            "longitude",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"validators": []},
            "username": {"validators": []},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Un utilisateur avec cet email existe déjà."
            )
        return value

    def validate_username(self, value):
        if " " in value:
            raise serializers.ValidationError(
                "Le nom d'utilisateur ne doit pas contenir d'espaces."
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return value

    def create(self, validated_data):
        city_name = validated_data.pop("city_name", None)
        postal_code = validated_data.pop("postal_code", None)
        latitude = validated_data.pop("latitude", None)
        longitude = validated_data.pop("longitude", None)
        password = validated_data.pop("password")
        new_user = User.objects.create(
            **validated_data,
            city_name=city_name,
            postal_code=postal_code,
            latitude=latitude,
            longitude=longitude,
            is_active=False,
        )
        new_user.set_password(password)
        new_user.save()
        return new_user
