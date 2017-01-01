from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from .models import Config


@admin.register(Config)
class ConfigAdmin(SingleModelAdmin):
    pass
