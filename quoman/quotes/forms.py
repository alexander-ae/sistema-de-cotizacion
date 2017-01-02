from django import forms
from .models import Quote


class QuoteForm(forms.ModelForm):

    class Meta:
        model = Quote
        fields = ('codigo', 'ruc', 'representante', 'tiempo_de_entrega', 'valida_hasta', 'forma_de_pago',
                  'costo_de_envio')
