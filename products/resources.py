import os
import urllib.request
from datetime import datetime

import requests
from dateutil import parser
from django.apps import apps
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Product, ProductImages


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
    date = Field(column_name='Актуальная_дата')
    characteristics = Field(column_name='Характеристики')
    images = Field(column_name='Картинки')
    price = Field(column_name='Цена')
    
    class Meta:
        batch_size = 1
        model = Product
        exclude = ('id', 'is_active', 'slug', )
        import_id_fields = ('article', )
        export_fields = ('name', 'category', 'brand', 'article', 'description',
                  'short_description', 'meta_keyword', 'meta_description', )

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        for row in dataset.dict:
            object = Product.objects.get(article=row['Артикул'])
            
            obj = parser.parse(str(row['Актуальная_дата']))
            date_str = datetime.strftime(obj, '%Y-%m-%d %H:%M:%S')
            price_kwargs = {'price': row['Цена'], 'date': date_str}
            setattr(object, 'price', price_kwargs)
            
            lists_raw = row['Картинки']

            lists = lists_raw.replace("[", " ").replace("]", " ").replace(" '", " ").replace("' ", " ").replace(", ", " ").replace("'", " ").split()
            
            # for url in lists:
            #     resp = requests.get(url)
            #     temp_file = NamedTemporaryFile()
            #     temp_file.write(resp.content)
            #     temp_file.flush()
                
            #     image = ProductImages()
            #     image.product = object
            #     image.alt = row['Наименование']
            #     image.image = File(temp_file, os.path.basename(resp.url))
            #     image.save()
        return super().after_import(dataset, result, using_transactions, dry_run, **kwargs)
