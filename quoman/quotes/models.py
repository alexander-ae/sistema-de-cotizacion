from django.core.urlresolvers import reverse
from django.db import models

from . import constants
from users.models import User


class Quote(models.Model):
    fecha_de_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)
    propietario_id = models.ForeignKey(User, verbose_name='Propietario', blank=True, null=True,
                                       on_delete=models.PROTECT)

    estado = models.CharField('Estado', max_length=24, choices=constants.COTIZACION_ESTADO,
                              default=constants.COTIZACION_PENDIENTE, blank=True)
    codigo = models.CharField('Código', max_length=12)
    ruc = models.CharField('RUC', max_length=12, blank=True)
    representante = models.CharField('Representante', max_length=96, blank=True)
    tiempo_de_entrega = models.CharField('Tiempo de Entrega', max_length=96, blank=True)
    valida_hasta = models.DateTimeField('Válida hasta', blank=True, null=True)
    forma_de_pago = models.TextField('Forma de pago', max_length=120)
    costo_de_envio = models.DecimalField('Costo de envío', max_digits=6, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['fecha_de_creacion']

    def __unicode__(self):
        return self.codigo

    def get_absolute_url(self):
        return reverse('quotes:edit', kwargs={'codigo': self.codigo})
