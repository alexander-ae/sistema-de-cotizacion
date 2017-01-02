from django.contrib import  admin

from .models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'estado', 'propietario_id')
    search_fields = ('codigo',)
    list_filter = ('estado',)
