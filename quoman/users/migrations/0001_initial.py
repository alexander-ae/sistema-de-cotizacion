# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-01 03:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(choices=[('ADMINISTRADOR', 'ADMINISTRADOR'), ('VENDEDOR', 'VENDEDOR')], default='VENDEDOR', max_length=32, verbose_name='Rol')),
                ('nombres', models.CharField(max_length=64, verbose_name='Nombres')),
                ('apellidos', models.CharField(max_length=64, verbose_name='Apellidos')),
                ('email', models.EmailField(max_length=64, verbose_name='Email')),
                ('telefono', models.CharField(blank=True, max_length=32, verbose_name='Teléfono')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
            },
        ),
    ]
