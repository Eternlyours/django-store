from django import forms
from django.forms import models, widgets
from .models import Cart, CartItem


# class CartItemModelForm(forms.Form):
#     product = forms.CharField(widget=widgets.TextInput(attrs={'readonly': 'readonly'}))
#     quantity = forms.IntegerField(min_value=0, label='Количество')

    # class Meta:
    #     model = CartItem
    #     fields = ('product' ,'quantity', )


# class CartModelForm(models.ModelForm):
#     class Meta:
#         model = Cart
#         fields = ('user', )


# CartInlineForm = models.inlineformset_factory(Cart, CartItem, form=CartItemModelForm, extra=0)