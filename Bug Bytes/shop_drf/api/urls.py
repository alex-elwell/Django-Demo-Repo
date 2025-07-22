"""URL routing for the API app."""

from api import views
from django.urls import path

urlpatterns = [
    path("products/", views.ProductListAPIView.as_view()),
    path("products/<int:pk>/", views.ProductDetailAPIView.as_view()),
    path("products/info/", views.product_info, name="product-info"),
    path("orders/", views.OrderListAPIView.as_view(), name="order-list"),
    path("orders/<uuid:pk>/", views.order_detail, name="order-detail"),
    path("user/orders/", views.UserOrderListAPIView.as_view(), name="user-orders"),
]
