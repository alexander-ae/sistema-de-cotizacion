from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ingresar/$', views.login_view, name='login'),
    url(r'^salir/$', views.logout_view, name='logout'),
    url(r'^perfil/$', views.profile, name='profile'),
    url(r'^perfil/password/$', views.update_password, name='update_password'),
    url(r'^olvido-password/$', views.forget_password, name='forget_password'),
    url(r'^cambiar-password/(?P<profile_id>\d+)/(?P<uuid>[^/]+)/$', views.set_password, name='set_password'),
]
