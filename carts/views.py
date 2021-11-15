from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from carts.forms import CartInlineForm, CartModelForm

from products.forms import ProductAddToCartForm
from .models import Cart, CartItem


class CartMixin:
    cart = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            carts = Cart.objects.filter(is_active=True)
            try:
                self.cart = carts.get(user=request.user)
            except ObjectDoesNotExist:
                pass
        return super().dispatch(request, *args, **kwargs)


class CartDetailView(CartMixin, DetailView):
    model = Cart
    template_name = 'cart-detail.html'
    context_object_name = 'cart'

    def get_object(self, queryset=None):
        return self.cart


class CartUpdateView(CartMixin, UpdateView):
    model = Cart
    template_name = 'cart-detail.html'
    form_class = CartModelForm    
    template_name_suffix = '_update_form'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['formset'] = CartInlineForm(instance=self.cart)
        return context
    
    def get_object(self, queryset=None):
        return self.cart

    