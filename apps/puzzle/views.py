import random

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.category.models import Category
from apps.utils.permissions import IsOwnerOrIsAdminOrReadOnly
from apps.puzzle.models import Puzzle
from apps.puzzle.serializers import PuzzleSerializer


class PuzzleViewSet(viewsets.ModelViewSet):
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get("category")
        brand_id = self.request.query_params.get("brand")
        city_name = self.request.query_params.get("city")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        if city_name:
            queryset = queryset.filter(owner__city__name__iexact=city_name)
        return queryset

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrIsAdminOrReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"])
    def random(self, request):
        categories = list(Category.objects.all())
        selected_categories = random.sample(categories, 4)
        result = []
        for category in selected_categories:
            puzzles = list(Puzzle.objects.filter(category=category, is_published=True))
            selected_puzzles = random.sample(puzzles, min(4, len(puzzles)))
            result.append(
                {
                    "puzzles": PuzzleSerializer(selected_puzzles, many=True).data,
                    "category": category.name,
                    "category_id": category.id,
                }
            )

        return Response(result)
