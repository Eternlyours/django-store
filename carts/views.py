import json

from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.serializers.json import DjangoJSONEncoder
from django.http.response import (HttpResponse, HttpResponseRedirect,
                                  JsonResponse)
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormMixin, UpdateView
from products.forms import ProductAddToCartForm

from carts.forms import CartInlineForm

from .models import Cart, CartItem


class FileJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, InMemoryUploadedFile):
            return o.read()
        return str(o)


class JSONResponsableMixin(FormMixin):

    def form_invalid(self, form):        
        response = json.dumps(form.errors)
        return JsonResponse({'errors': response}, content_type='application/json', status=400)

    def form_valid(self, form):
        response = json.dumps(form.cleaned_data, cls=FileJSONEncoder)
        return JsonResponse({'data': response}, content_type='application/json', status=200)


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
            return HttpResponseRedirect(reverse_lazy('cart-detail'))
        else:
            return self.render_to_response(self.get_context_data(formset=formset))


# class CartDetailView(FormMixin, CartMixin, DetailView):
#     queryset = Cart.objects.get_cart_items()
#     template_name = 'cart-detail.html'
#     context_object_name = 'cart'
#     form_class = CartInlineForm
#     success_url = '/cart/'

#     def get_object(self, queryset=None):
#         return self.cart

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context['formset'] = CartInlineForm(self.request.POST ,instance=self.cart)
#         else:
#             context['formset'] = CartInlineForm(instance=self.cart)
#         return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         formset = CartInlineForm(
#             request.POST, instance=self.object)
#         if formset.is_valid():
#             formset.save()
#             return self.form_valid(formset)
#         else:
#             return self.form_invalid(formset)


class CartItemAddToCartView(JSONResponsableMixin, View):
    form_class = ProductAddToCartForm

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            cart.add_to_cart(
                product=data.get('product'),
                quantity=data.get('quantity', 1)
            )    
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
