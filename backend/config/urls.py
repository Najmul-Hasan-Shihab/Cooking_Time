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
    
    # Phase 3: Gamification endpoints
    path('api/gamification/', include('apps.gamification.urls')),
    
    # Phase 3: User endpoints
    path('api/users/', include('apps.users.urls')),
]

# Import gamification views for direct routes
from apps.gamification.comments_views import update_comment, delete_comment, toggle_comment_like
from apps.gamification.leaderboard_views import leaderboard_by_xp, leaderboard_by_recipes, leaderboard_by_cooked
from apps.gamification.notification_views import (
    list_notifications, mark_notification_read, mark_all_read, 
    delete_notification, unread_count
)

# Add comment action routes
urlpatterns += [
    path('api/comments/<str:comment_id>/', update_comment, name='comment-update-put'),
    path('api/comments/<str:comment_id>/', delete_comment, name='comment-delete'),
    path('api/comments/<str:comment_id>/like/', toggle_comment_like, name='comment-like'),
]

# Add leaderboard routes
urlpatterns += [
    path('api/leaderboard/xp/', leaderboard_by_xp, name='leaderboard-xp'),
    path('api/leaderboard/recipes/', leaderboard_by_recipes, name='leaderboard-recipes'),
    path('api/leaderboard/cooked/', leaderboard_by_cooked, name='leaderboard-cooked'),
]

# Add notification routes
urlpatterns += [
    path('api/notifications/', list_notifications, name='notifications-list'),
    path('api/notifications/unread-count/', unread_count, name='notifications-unread-count'),
    path('api/notifications/mark-all-read/', mark_all_read, name='notifications-mark-all-read'),
    path('api/notifications/<str:notification_id>/read/', mark_notification_read, name='notification-mark-read'),
    path('api/notifications/<str:notification_id>/', delete_notification, name='notification-delete'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
