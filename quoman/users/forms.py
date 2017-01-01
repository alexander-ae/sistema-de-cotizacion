from django import forms
from django.contrib.auth import authenticate

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
