from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from core.models import Product, Category, Order, OrderItem, ReadySolution, ReadySolutionItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug' : ('title',)
    }


class ReadySolutionItemInline(admin.TabularInline):
    model = ReadySolutionItem
    fields = ('product', 'quantity', 'order')
    extra = 1
    verbose_name = 'Товар в составе'
    verbose_name_plural = 'Товары в составе'
    autocomplete_fields = ['product']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('product')


@admin.register(ReadySolution)
class ReadySolutionAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }
    list_display = ('title', 'persons_count', 'price', 'is_published', 'created_at')
    list_filter = ('is_published', 'persons_count', 'created_at')
    search_fields = ('title', 'description')
    inlines = [ReadySolutionItemInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'price', 'persons_count', 'is_published')
        }),
        ('Описание и изображение', {
            'fields': ('description', 'image_main')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug' : ('title',)
    }
    search_fields = ('title', 'description')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('product', 'quantity', 'price', 'item_total')
    readonly_fields = ('product', 'quantity', 'price', 'item_total')
    extra = 0
    can_delete = False
    
    def item_total(self, obj):
        """Общая сумма за товар"""
        if obj.pk:
            total = obj.quantity * obj.price
            return f'{total} ₽'
        return '-'
    item_total.short_description = 'Сумма'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'get_order_items', 'total_price', 'status', 'order_date', 'order_time', 'created_at')
    list_filter = ('status', 'order_date', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'delivery_address')
    readonly_fields = ('created_at', 'updated_at', 'total_price', 'get_order_items_detail')
    inlines = [OrderItemInline]
    list_editable = ('status',)  # Позволяет изменять статус прямо из списка
    actions = ['mark_as_new', 'mark_as_processing', 'mark_as_completed', 'mark_as_cancelled']
    
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('customer_name', 'customer_phone')
        }),
        ('Детали заказа', {
            'fields': ('order_date', 'order_time', 'delivery_address', 'total_price', 'status')
        }),
        ('Содержание заказа', {
            'fields': ('get_order_items_detail',),
            'classes': ('collapse',)
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_order_items(self, obj):
        """Показать товары в заказе в списке"""
        items = obj.items.all()
        if not items:
            return '-'
        
        items_list = []
        for item in items:
            items_list.append(f'{item.product.title} × {item.quantity}')
        
        # Показываем первые 3 товара, остальные скрываем
        display_items = items_list[:3]
        result = ', '.join(display_items)
        if len(items_list) > 3:
            result += f' <span style="color: #666;">(+{len(items_list) - 3} еще)</span>'
        
        return mark_safe(result)
    get_order_items.short_description = 'Товары'
    
    def get_order_items_detail(self, obj):
        """Детальное отображение товаров в заказе"""
        items = obj.items.all()
        if not items:
            return 'Заказ пуст'
        
        html = '<table style="width: 100%; border-collapse: collapse;">'
        html += '<thead><tr style="background: #f5f5f5;"><th style="padding: 8px; border: 1px solid #ddd;">Товар</th><th style="padding: 8px; border: 1px solid #ddd;">Количество</th><th style="padding: 8px; border: 1px solid #ddd;">Цена</th><th style="padding: 8px; border: 1px solid #ddd;">Сумма</th></tr></thead>'
        html += '<tbody>'
        
        for item in items:
            item_total = item.quantity * item.price
            html += f'<tr>'
            html += f'<td style="padding: 8px; border: 1px solid #ddd;">{item.product.title}</td>'
            html += f'<td style="padding: 8px; border: 1px solid #ddd; text-align: center;">{item.quantity}</td>'
            html += f'<td style="padding: 8px; border: 1px solid #ddd; text-align: right;">{item.price} ₽</td>'
            html += f'<td style="padding: 8px; border: 1px solid #ddd; text-align: right;"><strong>{item_total} ₽</strong></td>'
            html += f'</tr>'
        
        html += '</tbody>'
        html += '</table>'
        
        return mark_safe(html)
    get_order_items_detail.short_description = 'Содержание заказа'
    
    # Действия для массового изменения статуса
    def mark_as_new(self, request, queryset):
        queryset.update(status='new')
        self.message_user(request, f'{queryset.count()} заказ(ов) помечено(ы) как "Новый"')
    mark_as_new.short_description = 'Пометить как "Новый"'
    
    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')
        self.message_user(request, f'{queryset.count()} заказ(ов) помечено(ы) как "В обработке"')
    mark_as_processing.short_description = 'Пометить как "В обработке"'
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f'{queryset.count()} заказ(ов) помечено(ы) как "Завершен"')
    mark_as_completed.short_description = 'Пометить как "Завершен"'
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f'{queryset.count()} заказ(ов) помечено(ы) как "Отменен"')
    mark_as_cancelled.short_description = 'Пометить как "Отменен"'