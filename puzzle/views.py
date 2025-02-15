
from rest_framework import generics

from puzzle.models import Puzzle
from puzzle.serializers import PuzzleSerializer

class PuzzleListViewSet(generics.ListCreateAPIView):
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleSerializer


class PuzzleDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleSerializer
