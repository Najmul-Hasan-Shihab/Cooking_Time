"""
Views for gamification features
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Badge
from .badge_engine import (
    get_user_badges,
    get_all_badges_progress,
    check_and_award_badges,
    create_default_badges
)
from .serializers import BadgeSerializer, BadgeProgressSerializer


@api_view(['GET'])
def get_all_badges(request):
    """
    Get all available badges
    GET /api/gamification/badges
    """
    try:
        badges = Badge.objects(is_active=True)
        serializer = BadgeSerializer([badge.to_dict() for badge in badges], many=True)
        
        return Response({
            'badges': serializer.data,
            'total': len(serializer.data)
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_badges_view(request, user_id):
    """
    Get badges earned by a specific user
    GET /api/gamification/users/:id/badges
    """
    try:
        from apps.users.models import User
        
        # Get user
        user = User.objects.get(id=user_id)
        
        # Get earned badges
        badges = get_user_badges(user)
        
        return Response({
            'user_id': str(user.id),
            'username': user.username,
            'badges': badges,
            'total_badges': len(badges)
        }, status=status.HTTP_200_OK)
    
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_badge_progress_view(request):
    """
    Get current user's badge progress
    GET /api/gamification/badges/progress
    """
    try:
        user = request.user
        
        progress = get_all_badges_progress(user)
        
        return Response({
            'earned': progress['earned'],
            'in_progress': progress['in_progress'],
            'locked': progress['locked'],
            'stats': {
                'earned_count': len(progress['earned']),
                'in_progress_count': len(progress['in_progress']),
                'locked_count': len(progress['locked']),
                'total_count': len(progress['earned']) + len(progress['in_progress']) + len(progress['locked'])
            }
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_badges_view(request):
    """
    Manually trigger badge check for current user
    POST /api/gamification/badges/check
    """
    try:
        user = request.user
        
        newly_awarded = check_and_award_badges(user)
        
        return Response({
            'badges_earned': newly_awarded,
            'count': len(newly_awarded),
            'message': f'Earned {len(newly_awarded)} new badge(s)!' if newly_awarded else 'No new badges earned'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def initialize_badges(request):
    """
    Initialize default badges (admin only)
    POST /api/gamification/badges/initialize
    """
    try:
        # Check if user is admin (if authenticated)
        if request.user and hasattr(request.user, 'is_admin') and not request.user.is_admin:
            return Response({
                'error': 'Admin access required'
            }, status=status.HTTP_403_FORBIDDEN)
        
        count = create_default_badges()
        
        return Response({
            'message': f'Created {count} default badges' if count > 0 else 'Badges already exist',
            'count': count
        }, status=status.HTTP_201_CREATED if count > 0 else status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
