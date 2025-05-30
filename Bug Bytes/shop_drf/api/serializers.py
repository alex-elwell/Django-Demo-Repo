"""Serializer for all models in the shop_drf app."""

from typing import Any

from rest_framework import serializers

from .models import Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer[Product]):
    """Serializer for Product model."""

    class Meta:
        """Data to be serialized."""

        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "stock",
        )

    def validate_price(self, value: float) -> float:
        """Ensure the price is a positive number."""
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value


class OrderItemSerializer(serializers.ModelSerializer[OrderItem]):
    """Serializer for OrderItem model."""

    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2
    )

    class Meta:
        """Data to be serialized."""

        model = OrderItem
        fields = (
            "product_name",
            "product_price",
            "quantity",
            "partial_total",
        )


class OrderSerializer(serializers.ModelSerializer[Order]):
    """Serializer for Order model."""

    # Without this nested serializer, the items would just be the FK of the items in the order
    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        """Data to be serialized."""

        model = Order
        fields = (
            "order_id",
            "user",
            "created_at",
            "status",
            "items",
            "total_price",
        )

    def get_total_price(self, obj: Order) -> float:
        """Calculate the total price of the order."""
        return float(sum(item.partial_total for item in obj.items.all()))


class ProductInfoSerializer(serializers.Serializer[Any]):
    """Serializer for Product model with additional info."""

    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
