"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.http import JsonResponse
from django.shortcuts import redirect

def health_check(request):
    """Simple health check endpoint that doesn't require database."""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Django backend is running',
        'service': 'Travel Partner API'
    })

def root_redirect(request):
    """Redirect root URL to API documentation."""
    return redirect('/api/docs/')

urlpatterns = [
    # Root URL redirect
    path('', root_redirect, name='root'),
    
    # Admin Honeypot
    path('admin/honeypot/', include('admin_honeypot.urls')),
    
    path('admin/', admin.site.urls),
    
    # Health check endpoint (no database required)
    path('health/', health_check, name='health-check'),
    
    # API URLs
    path('api/auth/', include('apps.authentication.urls')),
    path('api/partner/', include('apps.partner.urls')),
    path('api/common/', include('apps.common.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Serve media files in both development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
