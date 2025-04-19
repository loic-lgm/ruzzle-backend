from django.contrib.auth import get_user_model
from rest_framework import serializers

from city.models import City
from city.serializers import CitySerializer


class UserSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "image",
            "city"
        ]


class UserRegistrationSerializer(serializers.ModelSerializer, UserSerializer):
    city_id = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model = get_user_model()
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
        extra_kwargs = {"password": {"write_only": True}}

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

        User = get_user_model()
        new_user = User.objects.create(email=email, username=username, city=city)
        new_user.set_password(password)
        new_user.save()
        return new_user
