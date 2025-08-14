import random

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.category.models import Category
from apps.utils.permissions import IsOwnerOrIsAdminOrReadOnly
from apps.puzzle.models import Puzzle
from apps.puzzle.serializers import PuzzleSerializer

from hashids import Hashids

hashids = Hashids(min_length=6, salt="ruzzlepuzzle")


class PuzzlePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class PuzzleViewSet(viewsets.ModelViewSet):
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PuzzlePagination

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(status__in=["swapped", "deleted"])
        category_id = self.request.query_params.get("category")
        brand_id = self.request.query_params.get("brand")
        city_name = self.request.query_params.get("city")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        if city_name:
            queryset = queryset.filter(owner__city__name__iexact=city_name)
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.exclude(owner=user)
        return queryset

    def get_object(self):
        """Get a puzzle via its hashid instead of id."""
        hashid = self.kwargs.get("pk")
        decoded = hashids.decode(hashid)
        if not decoded:
            raise NotFound("Puzzle introuvable")
        try:
            return Puzzle.objects.get(id=decoded[0])
        except Puzzle.DoesNotExist:
            raise NotFound("Puzzle introuvable")

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
        for category in selected_categories:
            puzzles = list(Puzzle.objects.filter(category=category, is_published=True))
            selected_puzzles = random.sample(puzzles, min(4, len(puzzles)))
        return Response(
            PuzzleSerializer(
                selected_puzzles, many=True, context={"request": request}
            ).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def mine(self, request):
        puzzles = Puzzle.objects.filter(owner=request.user).exclude(
            status__in=["swapped", "deleted"]
        )
        serializer = self.get_serializer(
            puzzles, many=True, context={"request": request}
        )
        return Response(serializer.data)

        return Response(result)
