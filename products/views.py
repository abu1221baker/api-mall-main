from django.shortcuts import get_object_or_404
from .models import Product, Order, Wishlist
from .serializer import ProductSerializer, OrderSerializer, WishlistSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


# -------------------- PRODUCT --------------------

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def product_list_create(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            # In a real app, you might want to associate the product with a vendor/user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------- ORDER --------------------

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def order_list_create(request):
    if request.method == "GET":
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        product_id = request.data.get("product_id")
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Check stock availability
        if product.stock < 1:
            return Response({"error": "Product out of stock"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # Decrement stock
            product.stock -= 1
            product.save()
            
            # Handle FKs in serializer.save() as requested
            serializer.save(
                user=request.user, 
                ordered_items=product,
                total_price=product.price
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if request.method == "GET":
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        # Allow status updates (partial update)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------- WISHLIST --------------------

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def wishlist_list_create(request):
    if request.method == "GET":
        wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        product_id = request.data.get("product")
        product = get_object_or_404(Product, id=product_id)
        
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            # Handle FKs in serializer.save() as requested
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def wishlist_detail(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk, user=request.user)
    
    if request.method == "GET":
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
    
    elif request.method == "DELETE":
        wishlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

