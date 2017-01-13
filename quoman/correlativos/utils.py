from .models import Correlativo

from datetime import date


def formatea_codigo(formato, numero):
    """
        Formatea un número en base a un string:

        formato   codigo   resultado
        #00        128       128
        #00         16        16
        000         16       016
         00        128       ERROR! (reiniciar cuenta)
    """
    total_caracteres = len(formato)
    total_ceros = formato.count('0')
    numero_str = str(numero)

    if len(numero_str) > total_caracteres:
        raise ValueError(u'Número de caracteres excedido')

    """
        lo siguiente genera algo similar a:
        '{:0>3}' -> completa con ceros hasta tres espacios
    """
    pre_codigo = ('{:0>' + str(total_ceros) + '}').format(numero_str)

    return pre_codigo


def formatea_prefix_postfix(pre_post):
    """
        Formatea el prefijo y postfijo.
    """
    hoy = date.today()

    FORMATO_ANIO = u'@AÑO'
    FORMATO_MES = u'@MES'
    FORMATO_DIA = u'@DIA'

    formato = pre_post.replace(FORMATO_ANIO, '{0:%Y}').replace(FORMATO_MES, '{0:%m}').replace(
        FORMATO_DIA, '{0:%d}')
    pre_post_formateado = formato.format(hoy)

    return pre_post_formateado


CODIGO_NO_GENERADO = ''


def genera_codigo(tipo):
    """ Genera códigos correlativos en base a la unidad operativa y el tipo """

    try:
        correlativo = Correlativo.objects.get(tipo=tipo)
    except:
        return CODIGO_NO_GENERADO

    actual = correlativo.actual
    incremento = correlativo.incremento
    formato = correlativo.formato
    inicio = correlativo.inicio
    termino = correlativo.termino
    prefijo = formatea_prefix_postfix(correlativo.prefijo)
    postfijo = formatea_prefix_postfix(correlativo.postfijo)

    if actual:
        numero_siguiente = actual + incremento
    else:
        numero_siguiente = inicio

    # término
    if termino:
        if numero_siguiente > termino:
            numero_siguiente = inicio

    try:
        pre_codigo = formatea_codigo(formato, numero_siguiente)
    except ValueError:
        numero_siguiente = correlativo.inicio
        pre_codigo = formatea_codigo(formato, numero_siguiente)

    codigo = u'{}{}{}'.format(prefijo, pre_codigo, postfijo)

    # actualizamos el número actual
    correlativo.actual = numero_siguiente
    correlativo.save()

    return codigo
