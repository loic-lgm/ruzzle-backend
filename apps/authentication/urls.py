from rest_framework.routers import DefaultRouter
from apps.authentication import views

router = DefaultRouter()
router.register("", views.AuthenticationViewSet, basename="authentication")

urlpatterns = router.urls
