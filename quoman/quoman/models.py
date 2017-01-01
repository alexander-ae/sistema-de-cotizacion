from django.db import models
from .constants import IGV


class Config(models.Model):
    logo = models.ImageField('Logo de la empresa', upload_to='config', blank=True, null=True)
    ruc = models.CharField('RUC', max_length=12, blank=True)
    direccion = models.CharField('Dirección', max_length=120, blank=True)
    igv = models.DecimalField('IGV', max_digits=3, decimal_places=1, default=IGV)
    detraccion_texto = models.TextField('Texto en caso de detracción', blank=True)

    class Meta:
        verbose_name = 'Configuración'
        verbose_name_plural = 'Configuración'

    def __unicode__(self):
        return 'Configuración'
