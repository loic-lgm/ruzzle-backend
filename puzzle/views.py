import random

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from category.models import Category
from permissions import IsOwnerOrIsAdminOrReadOnly
from puzzle.models import Puzzle
from puzzle.serializers import PuzzleSerializer


class PuzzleViewSet(viewsets.ModelViewSet):
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
