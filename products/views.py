from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from carts.views import CartMixin

from products.models import Product


class ProductListView(CartMixin, ListView):
    queryset = Product.objects.get_product_list().filter(is_active=True)
    template_name = 'product-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class ProductDetailView(CartMixin, DetailView):
    queryset = Product.objects.get_product_list().filter(is_active=True)
    template_name = 'product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context