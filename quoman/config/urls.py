from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('quoman.urls', namespace='quoman')),
    url(r'', include('users.urls', namespace='users')),
]
