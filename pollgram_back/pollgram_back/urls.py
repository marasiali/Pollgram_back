from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from pollgram_auth.views import verified

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('socialmedia.api_urls')),
    path('api/rest-auth/', include('pollgram_auth.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
