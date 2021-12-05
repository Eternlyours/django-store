import json

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.serializers.json import DjangoJSONEncoder
from django.http.response import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeletionMixin, FormMixin
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
            except Cart.DoesNotExist:
                self.cart = None
        return super().dispatch(request, *args, **kwargs)


class ItemCartAddMixin(FormMixin):
    model = CartItem
    form_class = ProductAddToCartForm
    object = None

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            message = cart.add_to_cart(
                product=data.get('product'),
                quantity=data.get('quantity', 1)
            )
            messages.success(request, message)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        return {'product': self.object.pk}


class ItemCartDeleteMixin(CartMixin, DeletionMixin):
    model = CartItem
    success_url = reverse_lazy('cart-detail')

    # @method_decorator(author_verification)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.cart.user != request.user:
            return HttpResponseRedirect(reverse_lazy('product-list'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        self.cart.check_cartitems_stock()
        return HttpResponseRedirect(success_url)


class JSONResponsableMixin(FormMixin):

    def form_invalid(self, form):        
        response = json.dumps(form.errors)
        return JsonResponse({'errors': response}, content_type='application/json', status=400)

    def form_valid(self, form):
        response = json.dumps(form.cleaned_data, cls=FileJSONEncoder)
        return JsonResponse({'data': response}, content_type='application/json', status=200)


class FileJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, InMemoryUploadedFile):
            return o.read()
        return str(o)
