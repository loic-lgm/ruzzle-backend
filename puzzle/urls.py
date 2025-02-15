from django.urls import path, include
from rest_framework.routers import DefaultRouter

from puzzle import views


router = DefaultRouter()
router.register("", views.PuzzleViewSet, basename="puzzle")

urlpatterns = [
    path("", include(router.urls)),
]
