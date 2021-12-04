import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.core.checks.messages import Error
from django.db import models
from django.contrib import messages
from products.models import Product
from django.shortcuts import get_object_or_404

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

    def check_cartitems_stock(self):
        if self.cartitems.count() == 0:
            return self.delete()
        return True

    def calculate_quantity_items_in_cart(self):
        quantity = 0
        for item in self.cartitems.all():
            quantity += item.quantity
        return quantity

    def calculate_price_items_in_cart(self):
        price = 0
        for item in self.cartitems.all():
            price += item.calculate_price_item()
        return price

    def check_update(self):
        if self.created_at == self.updated_at:
            return False
        return True

    def add_to_cart(self, product, quantity):
        cartitem = CartItem.add_item_to_cart(
            cart=self,
            product=product,
            quantity=quantity
        )
        return cartitem

    def remove_from_cart(self, product):
        return CartItem.objects.get(
            cart=self,
            product=product
        ).delete()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,
                             related_name='cartitems', verbose_name='Корзина')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Товар в корзине')
    quantity = models.IntegerField('Количество', default=1)

    def calculate_price_item(self):
        return self.quantity * self.product.price

    def check_the_quantity_of_goods(self):
        if self.product.quantity < self.quantity:
            return False
        return True

    def add_item_to_cart(cart, product, quantity):
        product = get_object_or_404(Product, pk=product)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )
        item.quantity = quantity
        item.save()
        return item
