from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from products.models import Product


class ProductListView(ListView):
    queryset = Product.objects.get_product_list().filter(is_active=True)
    template_name = 'product-list.html'


class ProductDetailView(DetailView):
    queryset = Product.objects.get_product_list().filter(is_active=True)
    template_name = 'product-detail.html'