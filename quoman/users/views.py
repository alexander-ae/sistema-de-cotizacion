from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from .forms import LoginForm
from .forms import UserProfileForm


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


def logout_view(request):
    return logout_then_login(request)


@login_required
def profile(request):

    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Perfil Actualizado')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'users/profile.html', locals())
