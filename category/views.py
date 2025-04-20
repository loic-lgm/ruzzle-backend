from rest_framework import mixins, viewsets

from category.models import Category
from category.serializers import CategorySerializer


class CategoryViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
