from django.db import models
from django.shortcuts import get_object_or_404

from products.models import Product


class CartManager(models.Manager):
    
    def get_cart_items(self):
        return self \
            .select_related('user') \
            .prefetch_related('cartitems') \
            .prefetch_related('cartitems__product') \
            .prefetch_related('cartitems__product__quantites') \
            .prefetch_related('cartitems__product__prices').all()


class CartItemManager(models.Manager):

    def add_item(self, cart, product, quantity):
        product = get_object_or_404(Product, pk=product)
        return self.create(
            cart=cart,
            product=product,
            quantity=quantity
        )