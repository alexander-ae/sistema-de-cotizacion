from django.contrib import  admin

from . import models


class QuoteReceiverInline(admin.TabularInline):
    model = models.QuoteReceiver
    extra = 0


class QuoteProductInline(admin.TabularInline):
    model = models.QuoteProduct
    extra = 0


@admin.register(models.Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'estado', 'propietario_id')
    search_fields = ('codigo',)
    list_filter = ('estado',)
    inlines = [QuoteReceiverInline, QuoteProductInline]


@admin.register(models.QuoteReceiver)
class QuoteReceiverAdmin(admin.ModelAdmin):
    pass


@admin.register(models.QuoteProduct)
class QuoteProductAdmin(admin.ModelAdmin):
    pass
