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
    quantity = forms.IntegerField(min_value=1, label='Количество', initial=1)
    product = forms.CharField(
        max_length=255, required=True, widget=forms.HiddenInput())

    def clean(self):
        data = super().clean()
        product = data.get('product')
        quantity = data.get('quantity')
        if get_object_or_404(Product, slug=product).quantity < quantity:
            raise ValidationError('Недостаточно товаров на складе')    
        return data