from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import LoginView, UserViewSet

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("login/", LoginView.as_view(), name="api_login"),
    path("", include(router.urls)),
]