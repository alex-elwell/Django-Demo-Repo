"""URL routing for the API app."""

from api import views
from django.urls import path

urlpatterns = [
    path("products/", views.product_list, name="product-list"),
    path("products/<int:pk>/", views.product_detail, name="product-detail"),
    
    path("orders/", views.order_list, name="product-list"),

]
