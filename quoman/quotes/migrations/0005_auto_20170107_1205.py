# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-07 17:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0004_auto_20170104_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='codigo',
            field=models.CharField(max_length=12, unique=True, verbose_name='Código'),
        ),
    ]
