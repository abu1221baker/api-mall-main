from django.shortcuts import get_object_or_404
from .models import Product, Order, Wishlist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

def serialize_product(product):
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "image_url": product.image_url,
        "stock": product.stock,
        "is_active": product.is_active,
        "created_at": product.created_at,
        "catogery": product.catogery
    }

def serialize_order(order):
    return {
        "id": order.id,
        "user": order.user.id,
        "ordered_items": serialize_product(order.ordered_items),
        "status": order.status,
        "total_price": str(order.total_price),
        "created_at": order.created_at
    }

def serialize_wishlist(wishlist):
    return {
        "id": wishlist.id,
        "user": wishlist.user.id,
        "product": serialize_product(wishlist.product),
        "added_at": wishlist.added_at
    }

# -------------------- PRODUCT --------------------

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def product_list_create(request):
    if request.method == "GET":
        products = Product.objects.all()
        data = [serialize_product(p) for p in products]
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        data = request.data
        try:
            product = Product.objects.create(
                name=data.get("name"),
                description=data.get("description", ""),
                price=data.get("price"),
                image_url=data.get("image_url", ""),
                stock=data.get("stock", 0),
                is_active=data.get("is_active", True),
                catogery=data.get("catogery", "")
            )
            return Response(serialize_product(product), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "GET":
        return Response(serialize_product(product))

    elif request.method == "PUT":
        data = request.data
        product.name = data.get("name", product.name)
        product.description = data.get("description", product.description)
        product.price = data.get("price", product.price)
        product.image_url = data.get("image_url", product.image_url)
        product.stock = data.get("stock", product.stock)
        product.is_active = data.get("is_active", product.is_active)
        product.catogery = data.get("catogery", product.catogery)
        product.save()
        return Response(serialize_product(product))

    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------- ORDER --------------------

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def order_list_create(request):
    if request.method == "GET":
        orders = Order.objects.filter(user=request.user)
        data = [serialize_order(o) for o in orders]
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        product_id = request.data.get("product_id")
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        if product.stock < 1:
            return Response({"error": "Product out of stock"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product.stock -= 1
            product.save()
            
            order = Order.objects.create(
                user=request.user,
                ordered_items=product,
                total_price=product.price,
                status="pending"
            )
            return Response(serialize_order(order), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if request.method == "GET":
        return Response(serialize_order(order))
    
    elif request.method == "PUT":
        data = request.data
        order.status = data.get("status", order.status)
        order.save()
        return Response(serialize_order(order))

    elif request.method == "DELETE":
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------- WISHLIST --------------------

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def wishlist_list_create(request):
    if request.method == "GET":
        wishlists = Wishlist.objects.filter(user=request.user)
        data = [serialize_wishlist(w) for w in wishlists]
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        product_id = request.data.get("product_id") or request.data.get("product")
        product = get_object_or_404(Product, id=product_id)
        
        try:
            wishlist, created = Wishlist.objects.get_or_create(
                user=request.user,
                product=product
            )
            return Response(serialize_wishlist(wishlist), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def wishlist_detail(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk, user=request.user)
    
    if request.method == "GET":
        return Response(serialize_wishlist(wishlist))
    
    elif request.method == "DELETE":
        wishlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

