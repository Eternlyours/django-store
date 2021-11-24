from django import forms
from django.forms import models, widgets
from .models import Cart, CartItem
from django.core.exceptions import ValidationError


class CartItemModelForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=0, label='Количество')

    class Meta:
        model = CartItem
        fields = ('quantity', )

    def clean(self):
        data = self.cleaned_data
        if data.get('quantity') == 0:
            data.update({'DELETE': True})
        if data.get('quantity') > self.instance.product.quantity:
            raise ValidationError('Недостаточно товаров на складе')      
        return data

CartInlineForm = models.inlineformset_factory(Cart, CartItem, form=CartItemModelForm, extra=0)