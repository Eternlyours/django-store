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
        return data
    
    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity > self.instance.product.quantity:
            i = int(quantity) - int(self.instance.product.quantity)
            msg = f'''
                Товара {self.instance.product.name} недостаточно
                {int(quantity) - int(self.instance.product.quantity)} штук,
                на складе {self.instance.product.quantity}, пожалуйста,
                введите корректное количество
            '''
            raise ValidationError(msg)
        return quantity

CartInlineForm = models.inlineformset_factory(Cart, CartItem, form=CartItemModelForm, extra=0)