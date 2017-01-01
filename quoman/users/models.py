from django.contrib.auth.models import User
from django.db import models

from . import constants


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField('Rol', max_length=32, choices=constants.ROLES, default=constants.ROL_VENDEDOR)
    nombres = models.CharField('Nombres', max_length=64)
    apellidos = models.CharField('Apellidos', max_length=64)
    email = models.EmailField('Email', max_length=64)
    telefono = models.CharField('Teléfono', max_length=32, blank=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __unicode__(self):
        return self.full_name()

    def full_name(self):
        return '{} {}'.format(self.nombres, self.apellidos)
