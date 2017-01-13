from django.db import models

CORRELATIVO_COTIZACION = '01'

CORRELATIVO_LISTA = (
    (CORRELATIVO_COTIZACION, 'Trabajador Portuario'),
)


class Correlativo(models.Model):
    tipo = models.CharField(max_length=2, choices=CORRELATIVO_LISTA, unique=True)
    prefijo = models.CharField(max_length=20, null=True, blank=True,
                               help_text='posibles variables: @AÑO , @MES, @DIA')
    postfijo = models.CharField(max_length=20, null=True, blank=True,
                                help_text='posibles variables: @AÑO , @MES, @DIA')
    formato = models.CharField(max_length=20, null=True, blank=True,
                               help_text='formato de ejemplo: #0000')
    inicio = models.IntegerField(default=1)
    incremento = models.IntegerField(default=1)
    termino = models.IntegerField(null=True, blank=True, verbose_name='Término')
    actual = models.IntegerField(default=0)

    class Meta:
        ordering = ['tipo']

    def __unicode__(self):
        return self.tipo
