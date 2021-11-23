from django.urls import path
from .views import CartDetailView, CartItemAddToCartView, CartItemUpdateView

urlpatterns = [
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/', CartItemAddToCartView.as_view(), name='add-to-cart'),
    path('cart/update/', CartItemUpdateView.as_view(), name='cart-update'),
]