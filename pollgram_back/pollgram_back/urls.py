from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('socialmedia.api_urls')),
    path('api/rest-auth/', include('pollgram_auth.api_urls')),
    path('api/poll/', include('poll.api_urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/notification/', include('notification_system.api_urls'), name='notification_system')
]

if not settings.IS_DOCKERIZED:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
