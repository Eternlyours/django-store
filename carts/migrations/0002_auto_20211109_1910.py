# Generated by Django 3.2.4 on 2021-11-09 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0009_auto_20210623_1842'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзины'},
        ),
        migrations.AddField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Время создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cart',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активность корзины'),
        ),
        migrations.AddField(
            model_name='cart',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Время обновления'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='cartitems', to='carts.cart', verbose_name='Корзина'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Товар в корзине'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Идентификатор'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
    ]
