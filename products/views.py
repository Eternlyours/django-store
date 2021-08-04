from django.views.generic.list import ListView

from products.models import Product


class ProductListView(ListView):
    queryset = Product.objects.get_product_list()
    template_name = 'products_list.html'
