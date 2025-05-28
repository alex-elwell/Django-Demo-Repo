"""Serializer for all models in the shop_drf app."""

from rest_framework import serializers

from .models import Product


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
