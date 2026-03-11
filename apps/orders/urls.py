from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import OrderItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r"", OrderViewSet, basename="order")

order_item_list = OrderItemViewSet.as_view({"get": "list", "post": "create"})
order_item_detail = OrderItemViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path("items/", order_item_list, name="order-item-list"),
    path("items/<int:pk>/", order_item_detail, name="order-item-detail"),
    path("", include(router.urls)),
]
