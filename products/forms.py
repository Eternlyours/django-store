from ckeditor.widgets import CKEditorWidget
from django import forms
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from carts.models import CartItem

from .models import Product


class CkeditorWidgetDescriptionMixin(forms.Form):
    description = forms.CharField(widget=CKEditorWidget(
        config_name='description'), label='Описание')


class ProductAdminModelFormOverride(CkeditorWidgetDescriptionMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     obj = self.instance
    #     ct = ContentType.objects.get_for_model(obj)
    #     fields = ProductTechnicalValue.objects.select_related('attribute').filter(
    #         content_type__pk=ct.pk, object_id=obj.id).all()
    #     self.fields = copy.deepcopy(self.base_fields)
    #     for field in fields:
    #         self.fields[field.attribute.slug] = forms.FloatField(
    #             required=True, label=field.attribute.name, initial=field.value_float)

    short_description = forms.CharField(widget=forms.Textarea(
        attrs={'cols': '0', 'rows': '0', 'style': 'width: 99%; height: 45px; resize: vertical;'}),
        label='Краткая информация')


class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=0, label='Количество', initial=1, required=True)
    product = forms.CharField(
        max_length=255, required=True, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        self.user = kwargs.pop('user', None)
        self.cart = kwargs.pop('cart', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        product = data.get('product')
        quantity = data.get('quantity')
        if get_object_or_404(Product, pk=product).quantity < quantity:
            self.add_error('quantity', 'Недостаточно товаров на складе')
        return data

    def clean_quantity(self):
        data = self.cleaned_data
        quantity = data.get('quantity')
        if quantity == 0 or quantity == '':
            self.add_error('quantity', 'Введите корректное количество!')
        return quantity

    
    