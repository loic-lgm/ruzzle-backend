from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from apps.message import views

router = DefaultRouter()
router.register("conversations", views.ConversationViewSet, basename="conversation")
router.register("", views.MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),
]
