from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .constants import COTIZACION_PENDIENTE
from .models import Quote
from .forms import QuoteForm, QuoteReceiverFormSet, QuoteProductFormSet
from .pdf import draw_pdf
from .pdf import envia_cotizacion
from .utils import pdf_response
from quoman.helpers import DefaultFormHelper
from users.constants import ROL_VENDEDOR, ROL_ADMINISTRADOR


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

    if cotizacion.propietario_id != usuario and cotizacion.propietario_id.is_superuser:
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


@login_required
def send_quote(request, codigo):
    data = {'status_code': 200}

    try:
        cotizacion = Quote.objects.get(codigo=codigo)
    except Quote.DoesNotExist:
        data['mensaje'] = 'No existe la cotización buscada'
        return JsonResponse(data, status_code=404)

    if cotizacion.estado != COTIZACION_PENDIENTE:
        data['status_code'] = 409
        data['mensaje'] = 'La cotización ya ha sido enviada'
    else:
        respuesta = envia_cotizacion(cotizacion)
        data['status_code'] = respuesta['status_code']
        data['mensaje'] = respuesta['mensaje']

    print(data)

    jsonResponse = JsonResponse(data)
    jsonResponse.status_code = data['status_code']

    return JsonResponse
