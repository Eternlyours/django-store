from django.apps import apps
from django.db.models.aggregates import Sum
from django.db.models.expressions import Value
from django.db.models.fields import IntegerField
from django.db.models.functions import Coalesce
from django.db.models.query_utils import Q


def get_and_calculate_the_quantity(obj):
    ProductAccouting = apps.get_model(
        'products_log', 'ProductAccouting')

    aggregate_values = {
        'coming': Coalesce(Sum('value', filter=Q(
            type=ProductAccouting.COMING), output_field=IntegerField()), Value(0)),
        'spending': Coalesce(Sum('value', filter=Q(
            type=ProductAccouting.SPENDING), output_field=IntegerField()), Value(0))
    }
    result = obj.quantities.all().aggregate(**aggregate_values)
    return result['coming'] - result['spending']


def set_price_or_quantity(obj, model, kwargs) -> None:
    model.objects.create(product=obj, **kwargs)
