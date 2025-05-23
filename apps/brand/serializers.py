from rest_framework import serializers

from apps.brand.models import Brand


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ["id", "name"]
