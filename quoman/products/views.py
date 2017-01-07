from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product
from .forms import ProductForm
from quoman.helpers import DefaultFormHelper


@login_required
def products_list(request):
    lista_productos = Product.objects.order_by('sku')

    return render(request, 'products/list.html', locals())


@login_required
def products_new(request):

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            producto = form.save()
            messages.add_message(request, messages.SUCCESS, 'Se registró el producto')

            return redirect(producto.get_absolute_url())
    else:
        form = ProductForm()

    helper = DefaultFormHelper

    return render(request, 'products/new_edit.html', locals())


@login_required
def products_edit(request, sku):
    # TODO: retornar a la lista de productos en caso se no encuentre el buscado
    producto = get_object_or_404(Product, sku=sku)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=producto)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Se actualizó el producto')

    else:
        form = ProductForm(instance=producto)

    helper = DefaultFormHelper
    
    return render(request, 'products/new_edit.html', locals())
