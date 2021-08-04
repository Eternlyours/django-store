from django.apps import apps
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Product


class ProductResource(resources.ModelResource):
    Brand = apps.get_model('products', 'Brand')
    Category = apps.get_model('products', 'Category')

    brand = Field(column_name='Производитель', attribute='brand',
                  widget=ForeignKeyWidget(Brand, 'name'))
    category = Field(column_name='Категория', attribute='category',
                     widget=ForeignKeyWidget(Category, 'name'))
    
    class Meta:
        batch_size = 5
        model = Product
        fields = ('name', 'category', 'brand', 'article', 'description',
                  'short_description', 'meta_keyword', 'meta_description', )

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        for row in dataset.dict:
            print(row)
            
        return super().after_import(dataset, result, using_transactions, dry_run, **kwargs)