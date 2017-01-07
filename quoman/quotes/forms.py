from django import forms
from django.forms.models import inlineformset_factory

from .models import Quote, QuoteReceiver, QuoteProduct
from quoman.helpers import DefaultFormHelper


class QuoteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)
        self.helper = DefaultFormHelper

    class Meta:
        model = Quote
        fields = ('codigo', 'ruc', 'representante', 'tiempo_de_entrega', 'valida_hasta', 'forma_de_pago',
                  'costo_de_envio')


QuoteReceiverFormSet = inlineformset_factory(Quote, QuoteReceiver, extra=0, can_delete=True,
                                             fields=('nombres', 'email'))

class QuoteProductForm(forms.ModelForm):
    class Meta:
        model = QuoteProduct
        fields = ('producto', 'sku', 'nombre', 'detalle', 'precio', 'cantidad')

    def __init__(self, *args, **kwargs):
        super(QuoteProductForm, self).__init__(*args, **kwargs)
        self.fields['producto'].widget.attrs.update({'class': 'producto'})
        self.fields['sku'].widget.attrs.update({'class': 'sku'})
        self.fields['nombre'].widget.attrs.update({'class': 'nombre'})
        self.fields['detalle'].widget.attrs.update({'class': 'detalle'})
        self.fields['precio'].widget.attrs.update({'class': 'precio'})

        self.helper = DefaultFormHelper

QuoteProductFormSet = inlineformset_factory(Quote, QuoteProduct, form=QuoteProductForm, extra=0, can_delete=True)
