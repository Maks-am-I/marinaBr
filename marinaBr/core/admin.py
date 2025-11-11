from django.contrib import admin

from core.models import Product, Category

admin.site.register(Category)
admin.site.register(Product)