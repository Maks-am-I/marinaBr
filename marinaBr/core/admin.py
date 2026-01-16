from django.contrib import admin
from django.utils.html import format_html

from core.models import Product, Category, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug' : ('title',)
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug' : ('title',)
    }


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price')
    extra = 0
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'total_price', 'status', 'order_date', 'order_time', 'created_at')
    list_filter = ('status', 'order_date', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'delivery_address')
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('customer_name', 'customer_phone')
        }),
        ('Детали заказа', {
            'fields': ('order_date', 'order_time', 'delivery_address', 'total_price', 'status')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
