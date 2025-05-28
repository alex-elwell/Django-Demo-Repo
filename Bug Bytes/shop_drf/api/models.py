import uuid
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser."""

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # last_login = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        """String representation of the User model."""
        return str(self.username)


class Product(models.Model):
    """Model representing a product in the shop."""

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveBigIntegerField()
    image = models.ImageField(upload_to="products/", null=True, blank=True)

    @property
    def in_stock(self) -> bool:
        """Check if the product is in stock."""
        return self.stock > 0

    def __str__(self) -> str:
        """String representation of the Product model."""
        return str(self.name)


class Order(models.Model):
    """Model representing an order placed by a user."""

    class StatusChoices(models.TextChoices):
        """Enumeration for order status choices."""

        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    products = models.ManyToManyField(Product, related_name="orders", blank=True)

    def __str__(self) -> str:
        """String representation of the Order model."""
        return f"Order {self.order_id} by {self.user.username} - {self.status}"


class OrderItem(models.Model):
    """Model representing an item in an order."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def partial_total(self) -> Decimal:
        """Calculate the total price for this order item."""
        return self.quantity * self.product.price

    def __str__(self) -> str:
        """String representation of the OrderItem model."""
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"
