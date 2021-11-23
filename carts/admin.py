from django.contrib import admin

from carts.models import Cart, CartItem


class CartItemInlineAdmin(admin.TabularInline):
    model = CartItem
    fields = ('product', 'get_product_price', 'calculate_price_item', 'quantity', )
    readonly_fields = ('calculate_price_item', 'get_product_price', )

    def get_product_price(self, obj):
        return obj.product.price


class CartAdmin(admin.ModelAdmin):
    fields = ('id', 'user', 'created_at', 'updated_at', 'is_active', 'calculate_price_items_in_cart', 'calculate_quantity_items_in_cart', )
    readonly_fields = ('id', 'created_at', 'updated_at', 'calculate_price_items_in_cart', 'calculate_quantity_items_in_cart', )
    inlines = (CartItemInlineAdmin, )



admin.site.register(Cart, CartAdmin)
