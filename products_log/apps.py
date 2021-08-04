from django.apps import AppConfig


class ProductsLogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products_log'
    verbose_name = 'Документы и журналы товаров'