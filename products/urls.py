from django.urls import path
from .views import *


urlpatterns = [
    # -------------------- PRODUCT --------------------
    path("products/", product_list_create, name="product-list-create"),
    path("products/<int:pk>/", product_detail, name="product-detail"),

    # -------------------- ORDERS --------------------
    path("orders/", order_list_create, name="order-list-create"),
    path("orders/<int:pk>/", order_detail, name="order-detail"),

    # -------------------- WISHLIST --------------------
    path("wishlist/", wishlist_list_create, name="wishlist-list-create"),
    path("wishlist/<int:pk>/", wishlist_detail, name="wishlist-detail"),
]
