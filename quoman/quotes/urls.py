from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^lista/$', views.quotes_list, name='list'),
    url(r'^nuevo/$', views.quotes_new, name='new'),
    url(r'^editar/(?P<codigo>[-_\w]+)/$', views.quotes_edit, name='edit'),
    url(r'^detalle/(?P<codigo>[-_\w]+)/$', views.quotes_detail, name='detail'),
    url(r'^pdf/(?P<codigo>[-_\w]+)/$', views.quotes_pdf, name='pdf'),
    url(r'^enviar/(?P<codigo>[-_\w]+)/$', views.send_quote, name='send_quote'),
]
