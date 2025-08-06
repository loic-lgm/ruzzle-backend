from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.user import views

router = DefaultRouter()
router.register("", views.UserViewSet, basename="user")

urlpatterns = [
    path("me/", views.me, name="me"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("refresh/", views.refresh, name="refresh"),
    path("register/", views.register, name="register"),
    path("<str:username>/", views.get_user_by_username, name="public-profile"),
    *router.urls,
]
