from django.contrib import admin

from .models import (
    Address,
    Brand,
    CartItem,
    Category,
    Color,
    Order,
    OrderItem,
    Product,
    ProductImage,
    ProductType,
    Size,
    Wishlist,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "brand", "selling_price", "stock", "is_featured", "is_new_arrival")
    list_filter = ("category", "product_type", "brand", "is_featured", "is_new_arrival")
    search_fields = ("name", "description", "brand__name")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("sizes", "colors")
    inlines = [ProductImageInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "price", "quantity", "line_total")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "payment_method", "total", "created_at")
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("id", "user__username", "full_name", "phone")
    inlines = [OrderItemInline]


admin.site.register(Category)
admin.site.register(ProductType)
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Address)
admin.site.register(Wishlist)
admin.site.register(CartItem)
