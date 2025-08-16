from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.notification import views


router = DefaultRouter()
router.register("", views.NotificationViewSet, basename="notification")

urlpatterns = [
    path("", include(router.urls)),
]
