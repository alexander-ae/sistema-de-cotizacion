from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Quote
from .forms import QuoteForm, QuoteReceiverFormSet, QuoteProductFormSet
from quoman.helpers import DefaultFormHelper


@login_required
def quotes_list(request):
    lista_cotizaciones = Quote.objects.order_by('codigo').select_related('propietario_id__userprofile')

    return render(request, 'quotes/list.html', locals())


@login_required
def quotes_new(request):
    usuario = request.user
    cotizacion = Quote()

    if request.method == 'POST':
        form = QuoteForm(request.POST, request.FILES, instance=cotizacion)
        quoteReceiverFormSet = QuoteReceiverFormSet(request.POST, instance=cotizacion)
        quoteProductFormSet = QuoteProductFormSet(request.POST, instance=cotizacion)

        if form.is_valid() and quoteReceiverFormSet.is_valid() and quoteProductFormSet.is_valid():
            cotizacion = form.save()
            cotizacion.propietario_id = usuario
            cotizacion.save()

            quoteReceiverFormSet.save()
            quoteProductFormSet.save()

            messages.add_message(request, messages.SUCCESS, 'Se registró la cotización')

            return redirect(cotizacion.get_absolute_url())
    else:
        form = QuoteForm()
        quoteReceiverFormSet = QuoteReceiverFormSet(instance=cotizacion)
        quoteProductFormSet = QuoteProductFormSet(instance=cotizacion)

    helper = DefaultFormHelper

    return render(request, 'quotes/new_edit.html', locals())


@login_required
def quotes_edit(request, codigo):
    # TODO: retornar a la lista de cotizaciones en caso se no encuentre el buscado
    cotizacion = get_object_or_404(Quote, codigo=codigo)

    if request.method == 'POST':
        form = QuoteForm(request.POST, request.FILES, instance=cotizacion)
        quoteReceiverFormSet = QuoteReceiverFormSet(request.POST, instance=cotizacion)
        quoteProductFormSet = QuoteProductFormSet(request.POST, instance=cotizacion)

        if form.is_valid() and quoteReceiverFormSet.is_valid() and quoteProductFormSet.is_valid():
            cotizacion = form.save()
            quoteReceiverFormSet.save()
            quoteProductFormSet.save()

            for form in quoteProductFormSet:
                form.save()

            messages.add_message(request, messages.SUCCESS, 'Se actualizó la cotización')
            return redirect(cotizacion.get_absolute_url())

    else:
        form = QuoteForm(instance=cotizacion)
        quoteReceiverFormSet = QuoteReceiverFormSet(instance=cotizacion)
        quoteProductFormSet = QuoteProductFormSet(instance=cotizacion)

    helper = DefaultFormHelper

    return render(request, 'quotes/new_edit.html', locals())


@login_required
def quotes_detail(request, codigo):
    try:
        cotizacion = Quote.objects.get(codigo=codigo)
    except Quote.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'No existe la cotización buscada')
        return redirect('quotes:list')


    fields = ('fecha_de_creacion', 'propietario_id', 'estado', 'codigo', 'ruc')

    return render(request, 'quotes/detail.html', locals())
