from django.urls import path
from .views import CartView, AddItemToCartView, RemoveItemFromCartView, CheckoutView, WishlistView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/<int:pk>/', AddItemToCartView.as_view(), name='cart_add'),
    path('remove/<int:pk>/', RemoveItemFromCartView.as_view(), name='cart_remove'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
]