from django.contrib import admin
from django.forms.fields import IntegerField
from django.forms.formsets import MAX_NUM_FORM_COUNT
from django.forms.models import (BaseInlineFormSet, ModelForm,
                                 inlineformset_factory)
from products.models import Product

from .models import (ProductAccouting, ProductDocumentExpense, ProductDocumentPrice,
                     ProductDocumentReceipt)


class ProductAccountingAdmin(admin.ModelAdmin):
    pass


class ProductDocumentExpenseAdmin(admin.ModelAdmin):
    pass


class ProductDocumentReceiptAdmin(admin.ModelAdmin):
    pass


class ProductTabularinfoBaseFormset(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def get_queryset(self):
        qs = super().get_queryset()
        return qs[:3]


class ProductDocumentMixin(admin.TabularInline):
    model = None
    extra = 0
    min_num = 1
    ordering = ('-date', )
    readonly_fields = ('date', )
    classes = ('collapse', )
    can_delete = False
    formset = ProductTabularinfoBaseFormset


class ProductDocumentReceiptAdminStackedInline(ProductDocumentMixin):
    model = ProductDocumentReceipt
    fields = ('date', 'value', )


class ProductDocumentPriceAdminTabularInfo(ProductDocumentMixin):
    model = ProductDocumentPrice
    fields = ('date', 'price', )


class ProductDocumentPriceAdmin(admin.ModelAdmin):
    pass


admin.site.register(ProductAccouting, ProductAccountingAdmin)
admin.site.register(ProductDocumentExpense, ProductDocumentExpenseAdmin)
admin.site.register(ProductDocumentReceipt, ProductDocumentReceiptAdmin)
admin.site.register(ProductDocumentPrice, ProductDocumentPriceAdmin)
