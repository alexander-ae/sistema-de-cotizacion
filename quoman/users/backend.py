# -*- coding: utf-8 -*-

from django.utils import timezone

from .models import UserProfile


class AuthBackend(object):
    ''' Backend que permite el login mediante el email del modelo UserProfile y la contraseña del modelo User '''

    def authenticate(self, username=None, password=None):
        try:
            userProfile = UserProfile.objects.get(email=username)
        except UserProfile.DoesNotExist:
            return None

        user = userProfile.user

        if user.check_password(password):
            user.last_login = timezone.now()
            user.save()
            return user

        return None

    def get_user(self, username):
        try:
            return UserProfile.objects.get(id=username).user
        except UserProfile.DoesNotExist:
            return None
