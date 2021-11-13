import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from products.models import Product

from .manager import CartManager


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cart', verbose_name='Покупатель')
    created_at = models.DateTimeField('Время создания', auto_now_add=True)
    updated_at = models.DateTimeField('Время обновления', auto_now=True)
    is_active = models.BooleanField('Активность корзины', default=True)

    objects = CartManager()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        if self.is_active:
            status = 'Активна'
        else:
            status = 'Неактивна'
        return f'Корзина {self.user} - {datetime.strftime(self.created_at, "%m/%d/%Y, %H:%M:%S")} {status}'

    def check_update(self):
        if self.created_at == self.updated_at:
            return False
        return True


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,
                             related_name='cartitems', verbose_name='Корзина')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Товар в корзине')
