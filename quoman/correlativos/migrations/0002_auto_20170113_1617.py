# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-13 21:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('correlativos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correlativo',
            name='formato',
            field=models.CharField(blank=True, help_text='formato de ejemplo: #0000', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='correlativo',
            name='postfijo',
            field=models.CharField(blank=True, help_text='posibles variables: @AÑO , @MES, @DIA', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='correlativo',
            name='prefijo',
            field=models.CharField(blank=True, help_text='posibles variables: @AÑO , @MES, @DIA', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='correlativo',
            name='tipo',
            field=models.CharField(choices=[('01', 'Cotizaciones')], max_length=2, unique=True),
        ),
    ]
