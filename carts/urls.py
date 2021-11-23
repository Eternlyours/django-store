from django.urls import path
from .views import CartDetailView, CartItemAddToCartView

urlpatterns = [
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/', CartItemAddToCartView.as_view(), name='add-to-cart'),
]