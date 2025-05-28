"""Populate the database with random users, products, and orders."""

import random

from api.models import Order, OrderItem, Product, User
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    """Populate the database with random users, products, and orders."""

    help = "Populate the database with random users, products, and orders."

    def handle(self, *args: object, **options: object) -> None:
        # Create users
        users = []
        for i in range(5):
            username = f"user{i+1}"
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com",
                    "first_name": f"First{i+1}",
                    "last_name": f"Last{i+1}",
                    "is_active": True,
                    "is_staff": False,
                    "is_superuser": False,
                    "date_joined": timezone.now(),
                },
            )
            users.append(user)
        products = []
        for i in range(10):
            product, _ = Product.objects.get_or_create(
                name=f"Product {i+1}",
                defaults={
                    "description": f"Description for product {i+1}",
                    "price": round(random.uniform(10, 100), 2),
                    "stock": random.randint(1, 50),
                    "image": None,
                },
            )
            products.append(product)
        orders = []
        for i in range(8):
            user = random.choice(users)
            order = Order.objects.create(
                user=user,
                created_at=timezone.now(),
                status=random.choice(
                    [
                        Order.StatusChoices.PENDING,
                        Order.StatusChoices.COMPLETED,
                        Order.StatusChoices.CANCELLED,
                    ]
                ),
            )
            # Add products to order
            order_products = random.sample(products, k=random.randint(1, 4))
            order.products.set(order_products)
            # Create order items
            for product in order_products:
                OrderItem.objects.create(
                    order=order, product=product, quantity=random.randint(1, 5)
                )
            orders.append(order)
