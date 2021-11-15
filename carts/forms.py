from django import forms
from django.forms import models, widgets
from .models import Cart, CartItem


class CartItemModelForm(models.ModelForm):
    product = forms.CharField(widget=widgets.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = CartItem
        fields = ('product' ,'quantity', )


class CartModelForm(models.ModelForm):
    class Meta:
        model = Cart
        fields = ('user', )


CartInlineForm = models.inlineformset_factory(Cart, CartItem, form=CartItemModelForm, extra=0)