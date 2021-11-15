from carts.views import CartMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.urls import reverse

from products.forms import ProductAddToCartForm
from products.models import Product


class ProductListView(CartMixin, ListView):
    queryset = Product.objects.get_product_list().filter(is_active=True)
    template_name = 'product-list.html'


class ProductDetailView(CartMixin, DetailView, FormView):
    queryset = Product.objects.get_product_list().filter(is_active=True)
    template_name = 'product-detail.html'
    context_object_name = 'product'
    form_class = ProductAddToCartForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('product-detail', kwargs={'slug': self.object.slug})

    def get_initial(self):
        return {'product': self.object.slug}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def form_valid(self, form):
        return super().form_valid(form)
