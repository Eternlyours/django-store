from django.http.response import Http404, HttpResponse, JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.base import ContextMixin
from django.contrib.auth.decorators import login_required

from products.models import Product

from .models import Cart


class CartMixin:
    cart = None
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            carts = Cart.objects.filter(is_active=True)
            self.cart = carts.get(user=request.user)
        return super().dispatch(request, *args, **kwargs)


class CartDetailView(CartMixin, DetailView):
    model = Cart
    template_name = 'cart-detail.html'
    context_object_name = 'cart'

    def get_object(self, queryset=None):
        return self.cart
