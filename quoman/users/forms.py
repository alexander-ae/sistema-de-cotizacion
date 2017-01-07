import uuid

from django import forms
from django.contrib.auth import authenticate
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.EmailField(label='Email')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            UserProfile.objects.get(email=username)
        except UserProfile.DoesNotExist:
            mensaje = 'El email no ha sido registrado'
            raise forms.ValidationError(mensaje)

        return username

    def auth(self):
        cleaned_data = self.cleaned_data
        return authenticate(username=cleaned_data['username'], password=cleaned_data['password'])


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('email', 'nombres', 'apellidos', 'telefono')


class PasswordUpdateForm(forms.Form):
    old_password = forms.CharField(label='Antigua Contraseña', widget=forms.PasswordInput)
    new_password = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput, min_length=6)

    def update_password(self, user):
        new_password = self.cleaned_data.get('new_password')
        user.set_password(new_password)
        user.save()


class RecoverPasswordForm(forms.Form):
    email = forms.EmailField(label='Email')

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            self.u = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            mensaje = 'El email no ha sido registrado'
            raise forms.ValidationError(mensaje)

        return email

    def send_mail(self):
        htmly = get_template('users/email_request_password.html')
        cd = self.cleaned_data
        cd['user'] = self.u
        cd['SITE'] = settings.SITE_URL
        d = Context(cd)

        html_content = htmly.render(d)
        asunto = 'Actualización de Contraseña'
        mail = '{0}<{1}>'.format(settings.PROJECT_NAME, settings.DEFAULT_FROM_EMAIL)
        destinatarios = [self.u.email]
        msg = EmailMessage(asunto, html_content, mail, destinatarios)
        msg.content_subtype = "html"
        msg.send()


class SetPasswordForm(forms.Form):
    uuid = forms.CharField(widget=forms.HiddenInput)
    email = forms.EmailField(label='Email')
    email.widget.attrs.update({'readonly': 'readonly'})
    password = forms.CharField(label='Nueva contraseña', min_length=6,
                               max_length=32, widget=forms.PasswordInput)

    def clean_email(self):
        uuid = self.cleaned_data['uuid']
        email = self.cleaned_data['email']
        try:
            self.u = UserProfile.objects.get(email=email, uuid=uuid)
        except UserProfile.DoesNotExist:
            raise forms.ValidationError('El email o la clave temporal son incorrectos!')

        return email

    def save(self):
        cd = self.cleaned_data
        usuario = self.u
        usuario.user.set_password(cd['password'])
        usuario.uuid = uuid.uuid4()
        usuario.save()
        usuario.user.save()

    def send_mail(self):
        htmly = get_template('users/email_recover_password.html')
        site = settings.SITE_URL
        cd = self.cleaned_data
        cd['SITE'] = settings.SITE_URL
        cd['user'] = self.u
        d = Context(cd)

        html_content = htmly.render(d)
        asunto = u'Actualización de Contraseña'
        mail = '{0}<{1}>'.format(settings.PROJECT_NAME,
                                 settings.DEFAULT_FROM_EMAIL)
        msg = EmailMessage(asunto, html_content, mail, [self.u.email])
        msg.content_subtype = "html"
        msg.send()
