from django.db import models
from django.db.models.query import Prefetch


class ProductQueryset(models.QuerySet):
    def only_active(self):
        return self.filter(is_active=True)

    def categories(self):
        return self.select_related('category')

    def brands(self):
        return self.select_related('brand')

    def images(self):
        return self.prefetch_related(
            Prefetch(
                'images',
                to_attr='images_attr'
            )
        )

    def prices(self):
        return self.prefetch_related('prices')

    def quantities(self):
        return self.prefetch_related('quantities')
