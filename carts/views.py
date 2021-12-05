from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.detail import DetailView

from carts.forms import CartInlineForm

from .mixins import CartMixin
from .models import Cart


class CartDetailView(CartMixin, DetailView):
    queryset = Cart.objects.get_cart_items()
    template_name = 'cart-detail.html'
    context_object_name = 'cart'

    def get_object(self, queryset=None):
        return self.cart

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        formset = CartInlineForm(instance=self.cart)
        return self.render_to_response(self.get_context_data(formset=formset))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        formset = CartInlineForm(
            request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
            self.object.check_cartitems_stock()
            return HttpResponseRedirect(reverse_lazy('cart-detail'))
        else:
            return self.render_to_response(self.get_context_data(formset=formset))

