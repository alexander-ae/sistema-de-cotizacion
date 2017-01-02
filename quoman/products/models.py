from django.db import models
from django.core.urlresolvers import reverse


class Product(models.Model):
    sku = models.CharField('SKU', max_length=32, unique=True,
                           help_text='Identificador único')
    nombre = models.CharField('Nombre', max_length=64)
    detalle = models.TextField('Detalle', blank=True)
    precio = models.DecimalField('Precio', max_digits=12, decimal_places=2,
                                 help_text='Precio en soles con dos decimales como máximo.')
    imagen = models.ImageField('Imagen', upload_to='productos', blank=True, null=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['sku']

    def __unicode__(self):
        return self.sku

    def get_absolute_url(self):
        return reverse('products:edit', kwargs={'sku': self.sku})
