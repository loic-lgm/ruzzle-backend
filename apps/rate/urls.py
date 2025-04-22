from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.rate import views


router = DefaultRouter()
router.register("", views.RateViewSet, basename="rate")

urlpatterns = [
    path("", include(router.urls)),
]
