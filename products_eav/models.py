from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify
from unidecode import unidecode


class ProductTechnicalAttribute(models.Model):
    TYPE_TEXT = 'text'
    TYPE_INT = 'int'
    TYPE_BOOL = 'bool'
    TYPE_FLOAT = 'float'
    TYPE_DATE = 'date'

    DATATYPE_CHOICES = (
        (TYPE_TEXT, 'Текст'),
        (TYPE_INT, 'Целое число'),
        (TYPE_BOOL, 'Логический тип'),
        (TYPE_FLOAT, 'Число с плавающей точкой'),
        (TYPE_DATE, 'Дата'),
    )

    slug = models.SlugField('Семантический URL')
    name = models.CharField('Наименование атрибута', max_length=255)
    data_type = models.CharField(
        'Тип значения', choices=DATATYPE_CHOICES, max_length=6)

    class Meta:
        verbose_name = 'Атрибут'
        verbose_name_plural = 'Атрибуты'

    def __str__(self):
        return f'{self.name} ({self.get_data_type_display()})'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)


class ProductTechnicalValue(models.Model):
    attribute = models.ForeignKey(
        ProductTechnicalAttribute, on_delete=models.CASCADE, related_name='values', verbose_name='Атрибут')

    value_text = models.CharField(
        'Текстовое значение', null=True, blank=True, max_length=100)
    value_int = models.IntegerField(
        'Целочисленное значение', null=True, blank=True)
    value_bool = models.BooleanField('Булево значение', null=True, blank=True)
    value_float = models.FloatField(
        'Числовое значение с точкой', null=True, blank=True)
    value_date = models.DateTimeField(
        'Значение даты и времени', null=True, blank=True)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name='Объект продукта', related_query_name='values')
    object_id = models.PositiveBigIntegerField('Идентификатор товара')
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Значение атрибута'
        verbose_name_plural = 'Значения атрибутов'

    def _get_value(self):
        if self.attribute is not None:
            return getattr(self, 'value_%s' % self.attribute.data_type)
        return ''

    def _set_value(self):
        if self.attribute is not None:
            return setattr(self, 'value_%s' % self.attribute.data_type)
        return ''

    value = property(_get_value, _set_value)

    def __str__(self):
        return f'{self.attribute.name} ({self.value}) {self.content_object.name}'
