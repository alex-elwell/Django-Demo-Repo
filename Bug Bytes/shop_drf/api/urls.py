"""URL routing for the API app."""

from api import views
from django.urls import path

urlpatterns = [
    path("products/", views.product_list, name="product-list"),
    path("products/<int:pk>/", views.product_detail, name="product-detail"),
    path("products/info/", views.product_info, name="product-info"),
    path("orders/", views.order_list, name="product-list"),
    path("orders/<uuid:pk>/", views.order_detail, name="order-detail"),
]
