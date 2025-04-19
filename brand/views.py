from rest_framework import mixins, viewsets

from brand.models import Brand
from brand.serializers import BrandSerializer


class BrandViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
