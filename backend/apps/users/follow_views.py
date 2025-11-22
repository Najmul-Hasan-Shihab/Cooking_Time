"""
User following system API endpoints
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_follow(request, user_id):
    """
    Follow or unfollow a user
    POST /api/users/{user_id}/follow/
    """
    try:
        # Get the user to follow/unfollow
        target_user = User.objects.get(id=user_id)
        current_user = request.user
        
        # Can't follow yourself
        if str(target_user.id) == str(current_user.id):
            return Response(
                {'error': 'You cannot follow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already following
        is_following = str(target_user.id) in current_user.following
        
        if is_following:
            # Unfollow
            current_user.following.remove(str(target_user.id))
            target_user.followers.remove(str(current_user.id))
            action = 'unfollowed'
        else:
            # Follow
            current_user.following.append(str(target_user.id))
            target_user.followers.append(str(current_user.id))
            action = 'followed'
            
            # Send notification
            try:
                from apps.gamification.notification_helpers import notify_new_follower
                notify_new_follower(target_user, current_user)
            except Exception as e:
                pass  # Don't fail if notification fails
        
        # Update counts
        current_user.following_count = len(current_user.following)
        target_user.followers_count = len(target_user.followers)
        
        current_user.save()
        target_user.save()
        
        return Response({
            'action': action,
            'is_following': not is_following,
            'followers_count': target_user.followers_count,
            'following_count': current_user.following_count
        })
        
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_followers(request, user_id):
    """
    Get list of user's followers
    GET /api/users/{user_id}/followers/?page=1&limit=20
    """
    try:
        user = User.objects.get(id=user_id)
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 20)), 50)
        
        # Get followers
        follower_ids = user.followers
        followers = User.objects(id__in=follower_ids)
        
        # Pagination
        total = followers.count()
        start = (page - 1) * limit
        end = start + limit
        
        results = []
        for follower in followers[start:end]:
            results.append({
                'id': str(follower.id),
                'username': follower.username,
                'level': follower.level,
                'xp': follower.xp,
                'followers_count': follower.followers_count,
                'is_following': str(follower.id) in request.user.following if request.user and hasattr(request.user, 'following') else False
            })
        
        return Response({
            'count': total,
            'page': page,
            'limit': limit,
            'total_pages': (total + limit - 1) // limit if total > 0 else 0,
            'results': results
        })
        
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_following(request, user_id):
    """
    Get list of users that this user follows
    GET /api/users/{user_id}/following/?page=1&limit=20
    """
    try:
        user = User.objects.get(id=user_id)
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 20)), 50)
        
        # Get following
        following_ids = user.following
        following = User.objects(id__in=following_ids)
        
        # Pagination
        total = following.count()
        start = (page - 1) * limit
        end = start + limit
        
        results = []
        for followed_user in following[start:end]:
            results.append({
                'id': str(followed_user.id),
                'username': followed_user.username,
                'level': followed_user.level,
                'xp': followed_user.xp,
                'followers_count': followed_user.followers_count,
                'is_following': str(followed_user.id) in request.user.following if request.user and hasattr(request.user, 'following') else False
            })
        
        return Response({
            'count': total,
            'page': page,
            'limit': limit,
            'total_pages': (total + limit - 1) // limit if total > 0 else 0,
            'results': results
        })
        
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_activity_feed(request):
    """
    Get activity feed from followed users
    GET /api/users/feed/?page=1&limit=20
    
    Shows recent recipes from users you follow
    """
    try:
        from apps.recipes.models import Recipe
        
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 20)), 50)
        
        # Get followed users
        following_ids = request.user.following
        
        if not following_ids:
            return Response({
                'count': 0,
                'page': page,
                'limit': limit,
                'total_pages': 0,
                'results': []
            })
        
        # Get authors
        followed_users = User.objects(id__in=following_ids)
        
        # Get recent recipes from followed users
        recipes = Recipe.objects(
            author__in=followed_users,
            is_published=True
        ).order_by('-created_at')
        
        # Pagination
        total = recipes.count()
        start = (page - 1) * limit
        end = start + limit
        
        results = []
        for recipe in recipes[start:end]:
            results.append({
                'id': str(recipe.id),
                'slug': recipe.slug,
                'title': recipe.title,
                'description': recipe.description,
                'author': {
                    'id': str(recipe.author.id),
                    'username': recipe.author.username,
                    'level': recipe.author.level,
                },
                'images': recipe.images,
                'difficulty': recipe.difficulty,
                'total_time': recipe.total_time,
                'rating_stats': {
                    'average': recipe.rating_stats.average,
                    'count': recipe.rating_stats.count
                },
                'created_at': recipe.created_at.isoformat() if recipe.created_at else None
            })
        
        return Response({
            'count': total,
            'page': page,
            'limit': limit,
            'total_pages': (total + limit - 1) // limit if total > 0 else 0,
            'results': results
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
