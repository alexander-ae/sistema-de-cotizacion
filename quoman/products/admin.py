from django.contrib import  admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nombre')
    search_fields = ('sku', 'nombre')
