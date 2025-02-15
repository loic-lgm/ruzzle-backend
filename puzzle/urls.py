from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from puzzle import views


urlpatterns = [
    path("", views.PuzzleListViewSet.as_view()),
    path("<int:pk>/", views.PuzzleDetailViewSet.as_view()),
]
