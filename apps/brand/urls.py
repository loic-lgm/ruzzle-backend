from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.brand import views


router = DefaultRouter()
router.register("", views.BrandViewSet, basename="brand")

urlpatterns = [
    path("", include(router.urls)),
]
