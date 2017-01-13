from django.contrib import admin
from .models import Correlativo


@admin.register(Correlativo)
class CorrelativoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'actual', 'prefijo', 'postfijo', 'formato')
