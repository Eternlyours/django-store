from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from .forms import ProductTechnicalValueForm
from .models import ProductTechnicalAttribute, ProductTechnicalValue


class ProductTechnicalValueInline(GenericStackedInline):
    model = ProductTechnicalValue
    form = ProductTechnicalValueForm
    extra = 0
    verbose_name = 'Характеристика товара'
    verbose_name_plural = 'Характеристики товаров'
    classes = ('collapse', )


class ProductTechnicalAttributeAdmin(admin.ModelAdmin):
    fields = ('slug', 'name', 'data_type', )
    readonly_fields = ('slug', )
    list_display = ('name', )
    list_display_links = ('name', )


admin.site.register(ProductTechnicalValue)
admin.site.register(ProductTechnicalAttribute, ProductTechnicalAttributeAdmin)
