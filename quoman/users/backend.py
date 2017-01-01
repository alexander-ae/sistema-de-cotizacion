# -*- coding: utf-8 -*-

from django.contrib.auth.hashers import check_password
from django.utils import timezone
# from logging import getLogger

from .models import UserProfile


class AuthBackend(object):

    def authenticate(self, username=None, password=None):
        try:
            userProfile = UserProfile.objects.get(email=username)
        except UserProfile.DoesNotExist:
            # log.debug(u'El email no es válido')
            return None

        user = userProfile.user

        if user.check_password(password):
            user.last_login = timezone.now()
            user.save()
            return user

        # log.debug(u'La contraseña es incorrecta')
        return None

    def get_user(self, username):
        # log.debug('get_user: {0}'.format(username))
        try:
            return UserProfile.objects.get(id=username).user
        except UserProfile.DoesNotExist:
            # log.debug('El usuario no existe')
            return None
