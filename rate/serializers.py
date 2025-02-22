from rest_framework import serializers

from rate.models import Rate
from user.serializers import UserSerializer


class RateSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    reviewed = UserSerializer()
    rating = serializers.IntegerField(min_value=0, max_value=5)

    class Meta:
        model = Rate
        fields = ["id", "rating", "comment", "reviewer", "reviewed", "created"]
