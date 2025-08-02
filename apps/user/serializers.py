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
        fields = ["id", "username", "email", "first_name", "last_name", "image", "city", "created_at"]


class UserRegistrationSerializer(UserSerializer):
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
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return value

    def validate_image(self, value):
        return validate_image(value, serializers=self)

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        city_id = validated_data["city_id"]

        city = None
        if city_id:
            try:
                city = City.objects.get(id=city_id)
            except City.DoesNotExist:
                raise serializers.ValidationError(
                    {"city_id": "La ville spécifiée n'existe pas."}
                )

        new_user = User.objects.create(email=email, username=username, city=city)
        new_user.set_password(password)
        new_user.save()
        return new_user
