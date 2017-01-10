from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import Quote
from users.constants import ROL_VENDEDOR, ROL_ADMINISTRADOR
from .forms import QuoteForm, QuoteReceiverFormSet, QuoteProductFormSet
from .pdf import draw_pdf
from .utils import pdf_response

from quoman.helpers import DefaultFormHelper


@login_required
def quotes_list(request):
    user = request.user

    if user.userprofile.rol == ROL_VENDEDOR:
        lista_cotizaciones = Quote.objects.filter(propietario_id=user
                                                  ).order_by('codigo').select_related('propietario_id__userprofile')
    elif user.userprofile.rol == ROL_ADMINISTRADOR or user.is_staff():
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
    usuario = request.user

    try:
        cotizacion = Quote.objects.get(codigo=codigo)
    except Quote.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'No existe la cotización buscada')
        return redirect('quotes:list')

    if cotizacion.propietario_id != usuario:
        messages.add_message(request, messages.WARNING, 'No cuenta con permisos para ver la cotización')
        return redirect('quotes:list')

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


@login_required
def quotes_pdf(request, codigo):
    try:
        cotizacion = Quote.objects.get(codigo=codigo)
    except Quote.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'No existe la cotización buscada')
        return redirect('quotes:list')

    return pdf_response(draw_pdf, 'cotizacion.pdf', cotizacion)
