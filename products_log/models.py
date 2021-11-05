import uuid
from datetime import date, datetime

from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from products.models import Product


class ProductAccouting(models.Model):
    COMING = '+'
    SPENDING = '-'

    TYPE_OF_ADMISSION = (
        (COMING, 'Приход'),
        (SPENDING, 'Раход'),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    value = models.PositiveIntegerField('Количество')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='quantities', verbose_name='Товар')
    date = models.DateTimeField('Актуальная дата')
    type = models.CharField(verbose_name='Тип поступления',
                            choices=TYPE_OF_ADMISSION, max_length=1)
    recorder = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name='Регистратор')
    object_id = models.PositiveIntegerField(verbose_name='ID регистратора')
    content_object = GenericForeignKey('recorder', 'object_id')

    class Meta:
        verbose_name = 'Учёт товаров'
        verbose_name_plural = 'Учёт товаров'

    def __str__(self):
        return f'{self.type} {self.id}'


class ProductDocumentReceipt(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Товар', related_name='documents_receipt')
    date = models.DateTimeField('Дата создания')
    value = models.PositiveIntegerField('Значение')
    accounting = GenericRelation(ProductAccouting)

    class Meta:
        verbose_name = 'Документ поступления товара'
        verbose_name_plural = 'Документы поступления товаров'

    def __str__(self):
        return f'Поступление №{self.id} от {self.date}'

    def save(self, *args, **kwargs) -> None:
        if not self.date:
            self.date = datetime.now()
        super().save(*args, **kwargs)
        ProductAccouting.objects.create(
            product=self.product,
            value=self.value,
            type=ProductAccouting.COMING,
            content_object=self,
            date=self.date
        )


class ProductDocumentExpense(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Товар', related_name='documents_expense')
    date = models.DateTimeField('Дата создания')
    value = models.PositiveIntegerField('Значение')
    accounting = GenericRelation(ProductAccouting)

    class Meta:
        verbose_name = 'Документ реализации товара'
        verbose_name_plural = 'Документ реализации товаров'

    def __str__(self):
        return f'Расход №{self.id} от {self.date}'

    def save(self, *args, **kwargs) -> None:
        if not self.date:
            self.date = datetime.now()
        super().save(*args, **kwargs)
        ProductAccouting.objects.create(
            product=self.product,
            value=self.value,
            type=ProductAccouting.SPENDING,
            content_object=self,
            date=self.date
        )


class ProductDocumentPrice(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='prices', verbose_name='Товар')
    price = models.DecimalField('Цена', max_digits=15, decimal_places=2)
    date = models.DateTimeField('Актуальная дата')

    class Meta:
        verbose_name = 'Регистр цен'
        verbose_name_plural = 'Регистры цен'

    def __str__(self):
        return f'{self.product} от {self.date}'
