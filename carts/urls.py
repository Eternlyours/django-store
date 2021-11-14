from django.urls import path
from .views import CartDetailView


urlpatterns = [
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/<>/'),
    path('cart/update/<>/'),
    path('cart/delete/<>/'),
]