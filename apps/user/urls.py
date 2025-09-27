from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.user import views

router = DefaultRouter()
router.register("", views.UserViewSet, basename="user")

urlpatterns = [
    path("profile/<str:username>/", views.get_user_by_username, name="public-profile"),
    *router.urls,
]
