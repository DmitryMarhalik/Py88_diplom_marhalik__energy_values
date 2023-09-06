from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from energy_values import settings
from app_evop.views import pageNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_evop.urls')),
    path('captcha/', include('captcha.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
