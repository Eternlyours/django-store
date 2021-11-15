from django.urls import path
from .views import CartDetailView, CartUpdateView


urlpatterns = [
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/update/', CartUpdateView.as_view()),
    # path('cart/delete/<>/'),
]