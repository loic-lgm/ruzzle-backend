from rest_framework import mixins, viewsets

from apps.city.models import City
from apps.city.serializers import CitySerializer


class CityViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = City.objects.all()
    serializer_class = CitySerializer
