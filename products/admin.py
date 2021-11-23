from django.contrib import admin
from django.contrib.admin.decorators import display
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from products_eav.admin import ProductTechnicalValueInline
from products_log.admin import ProductDocumentPriceAdminTabularInfo, ProductDocumentReceiptAdminStackedInline

from products.forms import ProductAdminModelFormOverride

from .models import Brand, Category, Product, ProductImages
from .resources import ProductResource


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    fields = ('image', 'get_tag_img', 'alt', )
    readonly_fields = ('get_tag_img', )
    classes = ('collapse', )


class ProductAdmin(ImportExportModelAdmin):
    list_display = ('article', 'name', 'category', 'price', 'quantity', 'get_thumb_image', 'is_active', )
    list_display_links = ('article', 'name', )
    list_select_related = ('brand', 'category', )
    readonly_fields = ('slug', 'quantity', 'price', 'get_thumb_image', )
    list_filter = ('brand__name', 'category__name', 'is_active', )
    search_fields = ('slug', 'article', 'name', 'category__name', 'brand__name', 'description', 'meta_keyword', )
    list_editable = ('is_active', )
    fieldsets = (
        ('Стандартная информация', {
            'fields': (
                ('slug', 'get_thumb_image',),
                'name',
                ('quantity', 'price'),
                ('article', 'is_active', ),
                ('brand', 'category'),
            )
        }),
        ('Объёмная информация', {
            'classes': ('collapse',),
            'fields': (
                'short_description',
                'description',
            )
        }),
        ('META данные', {
            'classes': ('collapse',),
            'fields': (
                'meta_description',
                'meta_keyword',
            )
        }),
    )
    inlines = [ProductDocumentReceiptAdminStackedInline, ProductDocumentPriceAdminTabularInfo,
               ProductImagesInline, ProductTechnicalValueInline, ]
    resource_class = ProductResource
    form = ProductAdminModelFormOverride
    # change_form_template = 'admin/products/change_form.html'

    @display(description='Изображение')
    def get_thumb_image(self, obj):
        img = obj.images.first()
        return mark_safe(f'<img src={img.image.url} width=150 height=100 style="object-fit:cover;">') 

    def get_queryset(self, request):
        return Product.objects.get_product_list()


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )


class BrandAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )
    fields = ('slug', 'name', 'image', 'description',
              'meta_description', 'meta_keyword',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
