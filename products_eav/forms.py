import copy
import datetime

from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime

from .models import ProductTechnicalAttribute, ProductTechnicalValue


class ProductTechnicalValueForm(forms.ModelForm):
    TYPE_TEXT = 'text'
    TYPE_INT = 'int'
    TYPE_BOOL = 'bool'
    TYPE_FLOAT = 'float'
    TYPE_DATE = 'date'

    DATATYPE_CHOICES = {
        TYPE_TEXT: forms.CharField,
        TYPE_INT: forms.IntegerField,
        TYPE_BOOL: forms.BooleanField,
        TYPE_FLOAT: forms.FloatField,
        TYPE_DATE: forms.SplitDateTimeField
    }

    value = forms.Field(label='Значение', required=False,
                        help_text='Перед записью значения нажмите на кнопку "Сохранить и продолжить редактирование"!')

    class Meta:
        model = ProductTechnicalValue
        exclude = ('value_text', 'value_int', 'value_bool',
                   'value_float', 'value_date', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self._create_dynamic_fields()
        except:
            pass

    def _create_dynamic_fields(self):
        self.fields = copy.deepcopy(self.base_fields)
        attribute = getattr(self.instance, 'attribute')
        value = self.instance

        field_options = {
            'label': getattr(attribute, 'name'),
            'initial': getattr(value, 'value')
        }
        type_attribute = getattr(attribute, 'data_type')

        if type_attribute == self.TYPE_DATE:
            field_options.update({
                'widget': AdminSplitDateTime
            })

        _FIELD = self.DATATYPE_CHOICES[type_attribute]
        self.fields['value'] = _FIELD(**field_options)

    def save(self, commit=True):
        instance = super().save(commit=False)
        value = self.cleaned_data.get('value', '')
        name = 'value_%s' % instance.attribute.data_type
        if not value:
            return super().save(commit=commit)
        setattr(instance, name, value)
        return super().save(commit=commit)
