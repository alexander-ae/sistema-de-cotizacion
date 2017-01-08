from django.core.urlresolvers import reverse
from django.db import models

from . import constants
from products.models import Product
from users.models import User
from quoman.models import Config


class Quote(models.Model):
    fecha_de_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)
    propietario_id = models.ForeignKey(User, verbose_name='Propietario', blank=True, null=True,
                                       on_delete=models.PROTECT)

    estado = models.CharField('Estado', max_length=24, choices=constants.COTIZACION_ESTADO,
                              default=constants.COTIZACION_PENDIENTE, blank=True)
    codigo = models.CharField('Código', max_length=12, unique=True)
    ruc = models.CharField('RUC', max_length=12, blank=True)
    representante = models.CharField('Representante', max_length=96, blank=True)
    tiempo_de_entrega = models.CharField('Tiempo de Entrega', max_length=96, blank=True)
    valida_hasta = models.DateTimeField('Válida hasta', blank=True, null=True)
    forma_de_pago = models.TextField('Forma de pago', max_length=120)
    costo_de_envio = models.DecimalField('Costo de envío', max_digits=6, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=9, decimal_places=2, default=0)

    igv = models.DecimalField('IGV', max_digits=3, decimal_places=1)

    class Meta:
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['fecha_de_creacion']

    def __str__(self):
        return self.codigo

    def save(self, *args, **kwargs):
        self.total = self.calcula_total()
        if not self.igv:
            config, created = Config.objects.get_or_create(pk=1)
            self.igv = config.igv

        super(Quote, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('quotes:edit', kwargs={'codigo': self.codigo})

    def get_detail_url(self):
        return reverse('quotes:detail', kwargs={'codigo': self.codigo})

    def calcula_total(self):
        ''' Incluye el costo de los productos, costo de envío e IGV '''

        subtotal = 0
        for producto in self.productos_a_cotizar.all():
            subtotal = subtotal + producto.cantidad * producto.precio

        total_antes_igv = subtotal + self.costo_de_envio
        total = total_antes_igv * (1 + self.igv/100)

        return total


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
    quote = models.ForeignKey(Quote, verbose_name='Cotización', related_name='productos_a_cotizar')
    producto = models.ForeignKey(Product, verbose_name='Producto', blank=True, null=True)
    sku = models.CharField('SKU', max_length=32, help_text='Identificador único')
    nombre = models.CharField('Nombre', max_length=64)
    detalle = models.TextField('Detalle', blank=True)
    precio = models.DecimalField('Precio', max_digits=12, decimal_places=2,
                                 help_text='Precio en soles con dos decimales como máximo.')
    cantidad = models.IntegerField('Cantidad', default=1)
    subtotal = models.DecimalField('Subtotal', max_digits=9, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Producto a cotizar'
        verbose_name_plural = 'Productos a cotizar'
        unique_together = ('quote', 'sku')

    def __str__(self):
        return self.sku

    def save(self, *args, **kwargs):
        self.subtotal = self.calcula_subtotal()
        super(QuoteProduct, self).save(*args, **kwargs)

    def calcula_subtotal(self):
        return self.precio * self.cantidad
