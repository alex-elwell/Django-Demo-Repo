from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer


@api_view(["GET"])
def product_list(_: Request) -> Response:
    """List all products in the database and
    return them as a JSON response.
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

    # Custom json response can be used as well

    # return JsonResponse({
    #     'data': serializer.data,
    # })


@api_view(["GET"])
def product_detail(_: Request, pk: int) -> Response:
    """Retrieve a single product by its primary key (pk)
    and return it as a JSON response.
    """
    product = get_object_or_404(Product, pk=pk)

    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(["GET"])
def order_list(_: Request) -> Response:
    """List all orders in the database and
    return them as a JSON response.
    """
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
