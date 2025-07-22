from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order, Product
from .serializers import OrderSerializer, ProductInfoSerializer, ProductSerializer

# Function-based views can be used to create a simple API
# @api_view(["GET"])
# def product_list(_: Request) -> Response:
#     """List all products in the database and
#     return them as a JSON response.
#     """
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

#     # Custom json response can be used as well

#     # return JsonResponse({
#     #     'data': serializer.data,
#     # })


# Class-based views can be used to create a more structured API
class ProductListAPIView(generics.ListAPIView[Product]):
    """Retrieve a list of all products in the database."""

    queryset = Product.objects.filter(stock__gt=0)  # Filter out products with no stock
    serializer_class = ProductSerializer
    #


# Function-based views can be used to retrieve a single product
# @api_view(["GET"])
# def product_detail(_: Request, pk: int) -> Response:
#     """Retrieve a single product by its primary key (pk)
#     and return it as a JSON response.
#     """
#     product = get_object_or_404(Product, pk=pk)

#     serializer = ProductSerializer(product)
#     return Response(serializer.data)


class ProductDetailAPIView(generics.RetrieveAPIView[Product]):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# @api_view(["GET"])
# def order_list(_: Request) -> Response:
#     """List all orders in the database and
#     return them as a JSON response.
#     """
#     orders = Order.objects.prefetch_related('items__product')
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)


class UserOrderListAPIView(generics.ListAPIView[Order]):
    """ Order List API View - to return only user orders"""
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=user)  # Filter orders by the logged-in user



class OrderListAPIView(generics.ListAPIView[Order]):
    """ Order List API View - to return only user orders"""
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer


@api_view(["GET"])
def order_detail(_: Request, pk: str) -> Response:
    """Retrieve a single order by its primary key (pk)
    and return it as a JSON response.
    """
    order = get_object_or_404(Order, order_id=pk)

    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(["GET"])
def product_info(_: Request) -> Response:
    """Retrieve all products with additional info"""
    products = Product.objects.all()
    serializer = ProductInfoSerializer(
        {
            "products": products,
            "count": len(products),
            "max_price": products.aggregate(max_price=Max("price"))["max_price"],
        }
    )
    return Response(serializer.data)
