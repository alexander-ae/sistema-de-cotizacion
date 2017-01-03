from django.core.urlresolvers import reverse
from django.db import models

from . import constants
from products.models import Product
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
    total = models.DecimalField('Total', max_digits=9, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['fecha_de_creacion']

    def __str__(self):
        return self.codigo

    def get_absolute_url(self):
        return reverse('quotes:edit', kwargs={'codigo': self.codigo})



class QuoteReceiver(models.Model):
    quote = models.ForeignKey(Quote, verbose_name='', on_delete=models.CASCADE)
    nombres = models.CharField('Nombres', max_length=64, blank=True)
    email = models.EmailField('Email')

    class Meta:
        verbose_name = 'Destinatario de la cotización'
        verbose_name_plural = 'Destinatarios de la cotización'

    def __str__(self):
        return self.email

    def full_email(self):
        if self.nombres:
            return '{}<{}>'.format(self.nombres, self.email)

        return self.email


class QuoteProduct(models.Model):
    quote = models.ForeignKey(Quote, verbose_name='Cotización')
    producto = models.ForeignKey(Product, verbose_name='Producto', blank=True, null=True)
    sku = models.CharField('SKU', max_length=32, unique=True,
                           help_text='Identificador único')
    nombre = models.CharField('Nombre', max_length=64)
    detalle = models.TextField('Detalle', blank=True)
    precio = models.DecimalField('Precio', max_digits=12, decimal_places=2,
                                 help_text='Precio en soles con dos decimales como máximo.')
    cantidad = models.IntegerField('Cantidad', default=1)
    subtotal = models.DecimalField('Subtotal', max_digits=9, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Producto a cotizar'
        verbose_name_plural = 'Productos a cotizar'

    def __str__(self):
        return self.sku