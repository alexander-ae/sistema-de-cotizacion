from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^lista/$', views.quotes_list, name='list'),
    url(r'^nuevo/$', views.quotes_new, name='new'),
    url(r'^editar/(?P<codigo>[-\w]+)/$', views.quotes_edit, name='edit'),
]
