from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^lista/$', views.products_list, name='list'),
    url(r'^nuevo/$', views.products_new, name='new'),
    url(r'^editar/(?P<sku>[-\w]+)/$', views.products_edit, name='edit'),
]
