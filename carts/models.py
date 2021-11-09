from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from datetime import datetime
from products.models import Product


class Cart(models.Model):
    id = models.UUIDField('Идентификатор', default=uuid4,
                          editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cart', verbose_name='Покупатель')
    created_at = models.DateTimeField('Время создания', auto_now_add=True)
    updated_at = models.DateTimeField('Время обновления', auto_now=True)
    is_active = models.BooleanField('Активность корзины', default=True)

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
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems', verbose_name='Корзина')
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name='Товар в корзине')



