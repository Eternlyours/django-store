from django.http.response import Http404, HttpResponse, JsonResponse
from django.views.generic.detail import DetailView

from products.models import Product

from .models import Cart


class CartDetailView(DetailView):
    model = Cart
    template_name = 'cart-detail.html'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('cartitems', 'cartitems__product').filter(is_active=True)

    def get_object(self, queryset=None):
        self.queryset = self.get_queryset()
        try:
            return self.queryset.get(user=self.request.user)
        except:
            return None
