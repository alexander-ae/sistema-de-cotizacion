from django import forms
from django.forms.models import inlineformset_factory
from .models import Quote, QuoteReceiver, QuoteProduct


class QuoteForm(forms.ModelForm):

    class Meta:
        model = Quote
        fields = ('codigo', 'ruc', 'representante', 'tiempo_de_entrega', 'valida_hasta', 'forma_de_pago',
                  'costo_de_envio')


QuoteReceiverFormSet = inlineformset_factory(Quote, QuoteReceiver, extra=0, can_delete=True,
                                             fields=('nombres', 'email'))

QuoteProductFormSet = inlineformset_factory(Quote, QuoteProduct, extra=0, can_delete=True,
                                             fields=('producto', 'sku', 'nombre', 'detalle', 'precio', 'cantidad'))
