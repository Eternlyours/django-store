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

    name = Field(column_name='Наименование', attribute='name')
    article = Field(column_name='Артикул', attribute='article')
    description = Field(column_name='Детальное_описание', attribute='description')
    short_description = Field(column_name='Краткое_описание', attribute='short_description')
    meta_keyword = Field(column_name='META_ключевые_слова', attribute='meta_keyword')
    meta_description = Field(column_name='META_описание', attribute='meta_description')
    characteristics = Field(column_name='Характеристики')
    images = Field(column_name='Картинки')
    price = Field(column_name='Цена')
    
    class Meta:
        batch_size = 5
        model = Product
        exclude = ('id', 'is_active', 'slug', )
        import_id_fields = ('article', )
        export_fields = ('name', 'category', 'brand', 'article', 'description',
                  'short_description', 'meta_keyword', 'meta_description', )

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        for row in dataset.dict:
            print(row['Характеристики'])
            
        return super().after_import(dataset, result, using_transactions, dry_run, **kwargs)