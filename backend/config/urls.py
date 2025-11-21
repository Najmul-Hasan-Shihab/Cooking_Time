"""
URL configuration for Recipe Website API
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def health_check(request):
    """Health check endpoint for Docker and monitoring"""
    return Response({
        'status': 'healthy',
        'message': 'Recipe Website API is running',
        'version': '0.1.0',
        'phase': 'Phase 0 - Development Environment Ready'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def api_root(request):
    """API root endpoint"""
    return Response({
        'message': 'Welcome to Recipe Website API',
        'version': '0.1.0',
        'endpoints': {
            'health': '/api/health/',
            'admin': '/admin/',
            'auth': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'logout': '/api/auth/logout/',
                'me': '/api/auth/me/',
                'refresh': '/api/auth/refresh/',
            },
            'recipes': {
                'list': '/api/recipes/',
                'search': '/api/recipes/search/',
                'detail': '/api/recipes/{slug}/',
                'mark_cooked': '/api/recipes/{slug}/mark_cooked/',
            },
            # Coming soon
            # 'users': '/api/users/',
        }
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health-check'),
    path('api/', api_root, name='api-root'),
    
    # Phase 1: Authentication endpoints
    path('api/auth/', include('apps.authentication.urls')),
    
    # Phase 1: Recipe endpoints
    path('api/recipes/', include('apps.recipes.urls')),
    
    # Phase 1: User endpoints (coming next)
    # path('api/users/', include('apps.users.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
