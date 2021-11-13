# Generated by Django 3.2.4 on 2021-11-13 08:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDocumentReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Дата создания')),
                ('value', models.PositiveIntegerField(verbose_name='Значение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents_receipt', to='products.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Документ поступления товара',
                'verbose_name_plural': 'Документы поступления товаров',
            },
        ),
        migrations.CreateModel(
            name='ProductDocumentPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Цена')),
                ('date', models.DateTimeField(verbose_name='Актуальная дата')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='products.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Регистр цен',
                'verbose_name_plural': 'Регистры цен',
            },
        ),
        migrations.CreateModel(
            name='ProductDocumentExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Дата создания')),
                ('value', models.PositiveIntegerField(verbose_name='Значение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents_expense', to='products.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Документ реализации товара',
                'verbose_name_plural': 'Документ реализации товаров',
            },
        ),
        migrations.CreateModel(
            name='ProductAccouting',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.PositiveIntegerField(verbose_name='Количество')),
                ('date', models.DateTimeField(verbose_name='Актуальная дата')),
                ('type', models.CharField(choices=[('+', 'Приход'), ('-', 'Раход')], max_length=1, verbose_name='Тип поступления')),
                ('object_id', models.PositiveIntegerField(verbose_name='ID регистратора')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quantities', to='products.product', verbose_name='Товар')),
                ('recorder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Регистратор')),
            ],
            options={
                'verbose_name': 'Учёт товаров',
                'verbose_name_plural': 'Учёт товаров',
            },
        ),
    ]
