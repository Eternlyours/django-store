from django.contrib import admin

from carts.models import Cart, CartItem


class CartItemInlineAdmin(admin.TabularInline):
    model = CartItem


class CartAdmin(admin.ModelAdmin):
    fields = ('id', 'user', 'created_at', 'updated_at', 'is_active', )
    readonly_fields = ('id', 'created_at', 'updated_at', )
    inlines = (CartItemInlineAdmin, )



admin.site.register(Cart, CartAdmin)
