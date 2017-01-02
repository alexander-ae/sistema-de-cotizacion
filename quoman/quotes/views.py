from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Quote
from .forms import QuoteForm


@login_required
def quotes_list(request):
    lista_cotizaciones = Quote.objects.order_by('codigo').select_related('propietario_id__userprofile')

    return render(request, 'quotes/list.html', locals())


@login_required
def quotes_new(request):
    usuario = request.user

    if request.method == 'POST':
        form = QuoteForm(request.POST, request.FILES)

        if form.is_valid():
            cotizacion = form.save()
            cotizacion.propietario_id = usuario
            cotizacion.save()

            messages.add_message(request, messages.SUCCESS, 'Se registró el producto')

            return redirect(cotizacion.get_absolute_url())
    else:
        form = QuoteForm()

    return render(request, 'quotes/new_edit.html', locals())


@login_required
def quotes_edit(request, codigo):
    # TODO: retornar a la lista de cotizaciones en caso se no encuentre el buscado
    cotizacion = get_object_or_404(Quote, codigo=codigo)

    if request.method == 'POST':
        form = QuoteForm(request.POST, request.FILES, instance=cotizacion)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Se actualizó la cotización')

    else:
        form = QuoteForm(instance=cotizacion)

    return render(request, 'quotes/new_edit.html', locals())
