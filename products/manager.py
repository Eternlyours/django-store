from django.apps import apps
from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.expressions import ExpressionWrapper, F, OuterRef, Subquery, Value
from django.db.models.fields import DecimalField, FloatField, IntegerField
from django.db.models.functions import Coalesce, Concat
from django.db.models.query import Prefetch
from django.db.models.query_utils import Q


class ProductManager(models.Manager):

    def get_product_list(self):
        ProductAccouting = apps.get_model(
            'products_log', 'ProductAccouting')
        ProductDocumentPrice = apps.get_model(
            'products_log', 'ProductDocumentPrice'
        )
        ProductImages = apps.get_model(
            'products', 'ProductImages'
        )

        alias_quantity = {
            '_coming': Coalesce(Sum('quantities__value', filter=Q(
                quantities__type=ProductAccouting.COMING), output_field=IntegerField()), Value(0)),
            '_spending': Coalesce(Sum('quantities__value', filter=Q(
                quantities__type=ProductAccouting.SPENDING), output_field=IntegerField()), Value(0))
        }

        annotate_quantity = {
            'actual_quantity': ExpressionWrapper(
                F('_coming') - F('_spending'), output_field=IntegerField()),
        }

        annotate_price = {
            'actual_price': Subquery(ProductDocumentPrice.objects.filter(
                product=OuterRef('pk')).order_by('-date').values('price')[:1],
                output_field=FloatField())
        }

        defer = (
            'meta_description',
            'meta_keyword',
            'description',
            'category__description',
            'category__icon',
            'category__image',
            'category__meta_description',
            'category__meta_keyword',
            'category__description',
            'brand__image',
            'brand__meta_description',
            'brand__meta_keyword',
            'brand__description'
        )
        
        list = super().get_queryset() \
            .select_related('brand', 'category') \
            .prefetch_related('prices', 'quantities') \
            .prefetch_related(
                Prefetch(
                    'images',
                    to_attr='images_attr'
                )) \
            .alias(
                **alias_quantity
        ) \
            .annotate(
                **annotate_quantity,
                **annotate_price
        ) \
        .defer(
            *defer
        )
        return list

    def get_quantity(self):
        ProductAccouting = apps.get_model(
            'products_log', 'ProductAccouting')
        return self.alias(
            coming=Coalesce(Sum('quantities__value', filter=Q(
                quantities__type=ProductAccouting.COMING), output_field=IntegerField()), Value(0)),
            spending=Coalesce(Sum('quantities__value', filter=Q(
                quantities__type=ProductAccouting.SPENDING), output_field=IntegerField()), Value(0)),
        ).annotate(
            actual_quantity=ExpressionWrapper(
                F('coming') - F('spending'), output_field=IntegerField())
        ).values('actual_quantity')

    def get_price(self):
        return self.order_by(
            '-prices__date').annotate(
            actual_price=F('prices__price'))
