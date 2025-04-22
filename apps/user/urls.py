from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.user import views

router = DefaultRouter()
router.register("", views.UserViewSet, basename="user")

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    *router.urls,
]
