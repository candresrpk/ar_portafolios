from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from my_apps.portafolios.views import custom_404_view


handler404 = custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('my_apps.portafolios.urls')),
    path('accounts/', include('my_apps.usuarios.urls')),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)