from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView, \
    SpectacularJSONAPIView

from energy_values import settings
from app_evop.views import page_not_found


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_evop.urls')),
    path('api/', include('api_evop.urls')),
    path('captcha/', include('captcha.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('api/docs/json/', SpectacularJSONAPIView.as_view(), name="schema-json"),
    path('api/redocs/', SpectacularRedocView.as_view(url_name='schema'), name='redocs'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
