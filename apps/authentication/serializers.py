from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.city.models import City

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    city_id = serializers.IntegerField(write_only=True, required=False)

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
            "city",
            "city_id",
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
        city = None
        city_id = validated_data.pop("city_id", None)
        if city_id:
            try:
                city = City.objects.get(id=city_id)
            except City.DoesNotExist:
                raise serializers.ValidationError(
                    {"city_id": "La ville spécifiée n'existe pas."}
                )

        password = validated_data.pop("password")
        new_user = User.objects.create(
            **validated_data,
            city=city,
            is_active=False,
        )
        new_user.set_password(password)
        new_user.save()
        return new_user
