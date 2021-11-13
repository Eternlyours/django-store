from django.db import models


class CartManager(models.Manager):
    
    def get_cart_items(self):
        return self \
            .select_related('user') \
            .prefetch_related('cartitems', 'cartitems__product')