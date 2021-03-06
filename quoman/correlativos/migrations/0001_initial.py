# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 23:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Correlativo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('01', 'Trabajador Portuario')], max_length=2, unique=True)),
                ('prefijo', models.CharField(blank=True, max_length=20, null=True)),
                ('postfijo', models.CharField(blank=True, max_length=20, null=True)),
                ('formato', models.CharField(blank=True, max_length=20, null=True)),
                ('inicio', models.IntegerField(default=1)),
                ('incremento', models.IntegerField(default=1)),
                ('termino', models.IntegerField(blank=True, null=True, verbose_name='Término')),
                ('actual', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['tipo'],
            },
        ),
    ]
