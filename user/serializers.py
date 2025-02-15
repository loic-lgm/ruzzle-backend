from dataclasses import fields
from django.contrib.auth import get_user_model
from rest_framework import serializers

# from user.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'image']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']

        User = get_user_model()
        new_user = User.objects.create(email=email, username=username)
        new_user.set_password(password)
        new_user.save()
        return new_user
