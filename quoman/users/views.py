from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from .forms import LoginForm
from .forms import UserProfileForm
from .forms import PasswordUpdateForm
from .forms import RecoverPasswordForm
from .forms import SetPasswordForm
from users.models import UserProfile


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
            messages.add_message(request, messages.SUCCESS, 'Perfil actualizado')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'users/profile.html', locals())


@login_required
def update_password(request):
    user = request.user

    if request.method == 'POST':
        form = PasswordUpdateForm(request.POST)

        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            if user.check_password(old_password):
                form.update_password(user)
                messages.add_message(request, messages.SUCCESS, 'Contraseña actualizada')
            else:
                messages.add_message(request, messages.ERROR, 'La contraseña actual no coincide')
    else:
        form = PasswordUpdateForm()

    return render(request, 'users/password_update.html', locals())


def forget_password(request):
    """ Pantalla para recuperar la contraseña """

    if request.method == 'POST':
        form = RecoverPasswordForm(request.POST)

        if form.is_valid():
            form.send_mail()
            messages.add_message(request, messages.SUCCESS, 'Se le enviaron las intrucciones por correo')
            return redirect('users:login')
    else:
        form = RecoverPasswordForm()

    return render(request, 'users/recover_password.html', locals())


def set_password(request, profile_id, uuid):

    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            form.save()
            form.send_mail()
            messages.add_message(request, messages.SUCCESS, 'Contraseña actualizada correctamente')
            return redirect(reverse('users:login'))
    else:
        try:
            user = UserProfile.objects.get(uuid=uuid, id=profile_id)
        except UserProfile.DoesNotExist:
            user = None
        form = SetPasswordForm(initial={'email': user.email, 'uuid': uuid})

    return render(request, 'users/set_password.html', locals())
