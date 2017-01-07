from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Product


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_tag = False

        self.helper.add_input(Submit('submit', 'Enviar'))

    class Meta:
        model = Product
        fields = ('sku', 'nombre', 'detalle', 'imagen', 'precio')
