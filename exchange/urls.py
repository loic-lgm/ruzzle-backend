from django.urls import path, include
from rest_framework.routers import DefaultRouter

from exchange import views


router = DefaultRouter()
router.register("", views.ExchangeViewSet, basename="exchange")

urlpatterns = [
    path("", include(router.urls)),
]
