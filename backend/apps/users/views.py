"""
User views for profile, stats, and user management
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from .models import User
from apps.recipes.models import Recipe
from apps.gamification.models import CookedRecipe, UserAction
from apps.gamification.badge_engine import get_user_badges
from apps.gamification.action_tracker import get_recent_activity, get_action_stats


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_stats(request, user_id):
    """
    Get comprehensive user statistics
    
    Returns:
    - user: Basic user info (id, username, avatar, bio, etc.)
    - xp_info: Current XP, level, level title, progress to next level
    - recipes: Created and cooked counts
    - badges: Earned badges count and list
    - social: Followers and following counts
    - join_date: Account creation date
    - recent_activity: Last 7 days of user actions
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get XP and level info
    xp_progress = user.get_xp_progress()
    
    # Count recipes created
    recipes_created = Recipe.objects(author=user).count()
    
    # Count recipes cooked
    recipes_cooked = CookedRecipe.objects(user=user).count()
    
    # Get badges earned
    user_badges = get_user_badges(user)
    badges_count = len(user_badges)
    
    # Get social stats (from User model)
    followers_count = len(user.followers) if user.followers else 0
    following_count = len(user.following) if user.following else 0
    
    # Get recent activity (last 7 days)
    recent_activity = get_recent_activity(user, days=7)
    
    # Get action statistics
    action_stats = get_action_stats(user)
    
    # Build response
    stats = {
        'user': {
            'id': str(user.id),
            'username': user.username,
            'email': user.email if str(request.user.id) == user_id or request.user.is_staff else None,  # Privacy
            'avatar_url': user.avatar_url,
            'bio': user.bio,
            'is_active': user.is_active,
        },
        'xp_info': {
            'total_xp': user.xp,
            'current_level': xp_progress['current_level'],
            'level_title': user.get_level_title(),
            'next_level': xp_progress['next_level'],
            'xp_in_current_level': xp_progress['current_level_xp'],
            'xp_for_next_level': xp_progress['next_level_xp'],
            'xp_needed': xp_progress['xp_needed'],
            'progress_percentage': xp_progress['progress_percentage'],
        },
        'recipes': {
            'created': recipes_created,
            'cooked': recipes_cooked,
        },
        'badges': {
            'total_earned': badges_count,
            'badges': user_badges  # get_user_badges already returns formatted dicts
        },
        'social': {
            'followers': followers_count,
            'following': following_count,
        },
        'join_date': user.created_at.isoformat() if user.created_at else None,
        'recent_activity': recent_activity[:20],  # Already formatted by get_recent_activity
        'action_stats': action_stats,
    }
    
    return Response(stats, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user_stats(request):
    """
    Get stats for the currently authenticated user
    """
    return get_user_stats(request, str(request.user.id))


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_profile(request, username):
    """
    Get user profile by username
    """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    return get_user_stats(request, str(user.id))


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update current user's profile
    
    Allowed fields:
    - username: string (unique)
    - email: string (unique)
    - bio: string (max 500 chars)
    - avatar_url: string (URL)
    - preferences: dict with cuisines, dietary_restrictions, favorite_tags
    """
    user = request.user
    data = request.data
    
    # Validate and update username
    if 'username' in data:
        new_username = data['username'].strip()
        if not new_username:
            return Response(
                {'error': 'Username cannot be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(new_username) > 50:
            return Response(
                {'error': 'Username must be 50 characters or less'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Check if username is already taken by another user
        if User.objects(username=new_username, id__ne=user.id).first():
            return Response(
                {'error': 'Username is already taken'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.username = new_username
    
    # Validate and update email
    if 'email' in data:
        new_email = data['email'].strip().lower()
        if not new_email:
            return Response(
                {'error': 'Email cannot be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Basic email validation
        if '@' not in new_email or '.' not in new_email.split('@')[1]:
            return Response(
                {'error': 'Invalid email format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Check if email is already taken by another user
        if User.objects(email=new_email, id__ne=user.id).first():
            return Response(
                {'error': 'Email is already taken'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.email = new_email
    
    # Update bio
    if 'bio' in data:
        bio = data['bio'].strip() if data['bio'] else ''
        if len(bio) > 500:
            return Response(
                {'error': 'Bio must be 500 characters or less'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.bio = bio
    
    # Update avatar URL
    if 'avatar_url' in data:
        avatar_url = data['avatar_url'].strip() if data['avatar_url'] else ''
        if len(avatar_url) > 500:
            return Response(
                {'error': 'Avatar URL must be 500 characters or less'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.avatar_url = avatar_url
    
    # Update preferences
    if 'preferences' in data:
        preferences = data['preferences']
        if not isinstance(preferences, dict):
            return Response(
                {'error': 'Preferences must be an object'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Merge with existing preferences
        current_prefs = user.preferences or {}
        
        if 'cuisines' in preferences:
            if not isinstance(preferences['cuisines'], list):
                return Response(
                    {'error': 'Cuisines must be an array'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            current_prefs['cuisines'] = preferences['cuisines']
        
        if 'dietary_restrictions' in preferences:
            if not isinstance(preferences['dietary_restrictions'], list):
                return Response(
                    {'error': 'Dietary restrictions must be an array'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            current_prefs['dietary_restrictions'] = preferences['dietary_restrictions']
        
        if 'favorite_tags' in preferences:
            if not isinstance(preferences['favorite_tags'], list):
                return Response(
                    {'error': 'Favorite tags must be an array'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            current_prefs['favorite_tags'] = preferences['favorite_tags']
        
        user.preferences = current_prefs
    
    # Update timestamp
    user.updated_at = timezone.now()
    
    # Save changes
    try:
        user.save()
    except Exception as e:
        return Response(
            {'error': f'Failed to update profile: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Return updated user data
    return Response(user.to_dict(), status=status.HTTP_200_OK)
