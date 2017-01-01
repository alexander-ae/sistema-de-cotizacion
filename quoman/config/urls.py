from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('quoman.urls', namespace='quoman')),
    url(r'', include('users.urls', namespace='users')),
    url(r'^productos/', include('products.urls', namespace='products')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
