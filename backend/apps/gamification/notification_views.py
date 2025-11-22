"""
Notification API endpoints
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .notification_model import Notification


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_notifications(request):
    """
    Get user's notifications
    GET /api/notifications/?page=1&limit=20&unread_only=false
    """
    try:
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 20)), 50)
        unread_only = request.GET.get('unread_only', 'false').lower() == 'true'
        
        # Build query
        query = {'recipient': request.user.id}
        if unread_only:
            query['is_read'] = False
        
        # Get notifications
        notifications = Notification.objects(**query).order_by('-created_at')
        
        # Pagination
        total = notifications.count()
        start = (page - 1) * limit
        end = start + limit
        
        return Response({
            'count': total,
            'unread_count': Notification.objects(recipient=request.user.id, is_read=False).count(),
            'page': page,
            'limit': limit,
            'total_pages': (total + limit - 1) // limit if total > 0 else 0,
            'results': [notif.to_dict() for notif in notifications[start:end]]
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    """
    Mark a notification as read
    POST /api/notifications/{id}/read/
    """
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user.id)
        
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            notification.save()
        
        return Response({
            'message': 'Notification marked as read',
            'notification': notification.to_dict()
        })
        
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_read(request):
    """
    Mark all notifications as read
    POST /api/notifications/mark-all-read/
    """
    try:
        notifications = Notification.objects(recipient=request.user.id, is_read=False)
        count = notifications.count()
        
        now = datetime.utcnow()
        for notif in notifications:
            notif.is_read = True
            notif.read_at = now
            notif.save()
        
        return Response({
            'message': f'{count} notifications marked as read',
            'count': count
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request, notification_id):
    """
    Delete a notification
    DELETE /api/notifications/{id}/
    """
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user.id)
        notification.delete()
        
        return Response({
            'message': 'Notification deleted'
        })
        
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_count(request):
    """
    Get count of unread notifications
    GET /api/notifications/unread-count/
    """
    try:
        count = Notification.objects(recipient=request.user.id, is_read=False).count()
        
        return Response({
            'unread_count': count
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
