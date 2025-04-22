from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.category import views


router = DefaultRouter()
router.register("", views.CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),
]
