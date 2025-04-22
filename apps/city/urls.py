from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.city import views


router = DefaultRouter()
router.register("", views.CityViewSet, basename="city")

urlpatterns = [
    path("", include(router.urls)),
]
