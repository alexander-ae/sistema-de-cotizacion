from django.conf.urls import url

from . import views
from . import api


urlpatterns = [
    url(r'^lista/$', views.products_list, name='list'),
    url(r'^nuevo/$', views.products_new, name='new'),
    url(r'^editar/(?P<sku>[-\w]+)/$', views.products_edit, name='edit'),

    # api
    url(r'^api/(?P<pk>[0-9]+)/$', api.ProductDetail.as_view(), name='api_detail'),
]
