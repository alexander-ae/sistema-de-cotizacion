from django.contrib.auth import login
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext as ctx
from django.shortcuts import render, redirect

from .forms import LoginForm


def login_view(request):
    # log.info('VIEW: login_view')

    if request.user.is_authenticated():
        return redirect(reverse('auth:logged_view'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.auth()
            if user is not None:
                if user.is_active:
                    # user.last_login = datetime.now()
                    # user.save()
                    login(request, user)

                    location = request.GET.get('next', None)

                    if location:
                        return redirect(location)

                    return redirect(reverse('quoman:home'))
                else:
                    messages.add_message(request, messages.WARNING,
                        'El usuario no se encuentra activo')
            else:
                messages.add_message(request, messages.WARNING,
                        u'El email y contraseña son inválidos')
        else:
            print('Error de formulario')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', locals())
