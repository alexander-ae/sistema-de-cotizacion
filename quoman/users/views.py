from django.contrib.auth import login
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from .forms import LoginForm


def login_view(request):

    if request.user.is_authenticated():
        return redirect(reverse('quoman:dashboard'))

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.auth()

            if user is not None:
                if user.is_active:
                    login(request, user)

                    location = request.GET.get('next', None)

                    if location:
                        return redirect(location)

                    return redirect(reverse('quoman:dashboard'))
                else:
                    messages.add_message(request, messages.WARNING,
                        'El usuario no se encuentra activo')
            else:
                messages.add_message(request, messages.WARNING,
                        'El email y contraseña son inválidos')
        else:
            messages.add_message(request, messages.WARNING, 'Error de formulario')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', locals())
