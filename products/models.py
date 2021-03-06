from django.apps import apps
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel, TreeForeignKey
from unidecode import unidecode

from .manager import ProductManager
from .utils import get_and_calculate_the_quantity, set_price_or_quantity


class Product(models.Model):
    slug = models.SlugField('Семантический URL', unique=True, max_length=255, db_index=True)
    name = models.CharField('Наименование', max_length=255, db_index=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE,
                              to_field='name', default='Stihl', verbose_name='Производитель')
    article = models.CharField('Артикул', unique=True, max_length=255, db_index=True)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, to_field='name', verbose_name='Категория')
    is_active = models.BooleanField('Отображать на сайте', default=True)
    description = models.TextField('Описание')
    short_description = models.CharField('Короткое описание', max_length=255)
    meta_keyword = models.TextField(
        'META Ключевые слова', null=True, blank=True)
    meta_description = models.TextField('META Описание', null=True, blank=True)

    objects = ProductManager()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug',), )

    def __str__(self) -> str:
        return f'{self.article} {self.name}'

    def get_absolute_url(self):
        return reverse_lazy('product-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{self.article} - {unidecode(self.name)}'
            self.slug = slugify(slug)
        return super().save(*args, **kwargs)

    def _get_quantity(self):
        if self.quantities.exists():
            return get_and_calculate_the_quantity(self)
        return 0
    _get_quantity.short_description = 'Количество'

    def _set_quantity(self, kwargs) -> None:
        ProductDocumentReceipt = apps.get_model('products_log', 'ProductDocumentReceipt')
        set_price_or_quantity(self, ProductDocumentReceipt, kwargs)
    _set_quantity.short_description = 'Быстрая запись поступления товара'
    
    quantity = property(_get_quantity, _set_quantity)

    def _get_price(self):
        if self.prices.exists():
            return getattr(self.prices.last(), 'price')
        return 0
    _get_price.short_description = 'Стоимость'    

    def _set_price(self, kwargs) -> None:
        ProductDocumentPrice = apps.get_model('products_log', 'ProductDocumentPrice')
        set_price_or_quantity(self, ProductDocumentPrice, kwargs)
    _set_price.short_description = 'Быстрая запись актуальной цены'    

    price = property(_get_price, _set_price)


class Brand(models.Model):
    slug = models.SlugField('Семантический URL', unique=True)
    name = models.CharField('Наименование', unique=True, max_length=100)
    description = models.TextField(
        'Описание производителя', null=True, blank=True)
    image = models.ImageField(
        'Картинка', upload_to='upload/brand/images/%Y/%m/%d/')
    meta_keyword = models.TextField(
        'META Ключевые слова', null=True, blank=True)
    meta_description = models.TextField('META Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return f'Производитель - {self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)


class Category(MPTTModel):
    slug = models.SlugField('Семантический URL', unique=True)
    name = models.CharField('Наименование', unique=True, max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    description = models.TextField('Описание категории', null=True, blank=True)
    image = models.ImageField(
        'Картинка', upload_to='upload/category/images/%Y/%m/%d/')
    icon = models.FileField(
        'Иконка', upload_to='upload/category/icons/%Y/%m/%d/')
    meta_keyword = models.TextField(
        'META Ключевые слова', null=True, blank=True)
    meta_description = models.TextField('META Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)


class ProductImages(models.Model):
    image = models.ImageField(
        'Картинка', upload_to='upload/images/images/%Y/%m/%d/')
    alt = models.CharField('Alt атрибут', null=True,
                           blank=True, max_length=255)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return self.image.url

    def get_tag_img(self):
        return mark_safe(f'<img src="{self.image.url}" height="150px" width="200px" style="object-fit: cover;" />')
    get_tag_img.short_description = 'Картинка'
    get_tag_img.allow_tags = True
