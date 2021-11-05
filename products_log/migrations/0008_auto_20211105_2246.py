# Generated by Django 3.2.4 on 2021-11-05 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_log', '0007_alter_productaccouting_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productaccouting',
            name='date',
            field=models.DateTimeField(verbose_name='Актуальная дата'),
        ),
        migrations.AlterField(
            model_name='productdocumentprice',
            name='date',
            field=models.DateTimeField(verbose_name='Актуальная дата'),
        ),
        migrations.AlterField(
            model_name='productdocumentreceipt',
            name='date',
            field=models.DateTimeField(verbose_name='Дата создания'),
        ),
    ]
