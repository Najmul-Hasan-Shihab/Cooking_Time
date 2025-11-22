"""
Views for comments system
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from .models import Comment
from apps.recipes.models import Recipe
from apps.users.models import User
from apps.gamification.action_tracker import track_comment_posted
from apps.gamification.badge_engine import check_and_award_badges


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def comments_list_create(request, slug):
    """
    List or create comments on a recipe
    GET /api/recipes/:slug/comments/?page=1&limit=20
    POST /api/recipes/:slug/comments/
    Body: { "content": "comment text" }
    """
    try:
        # Get recipe
        recipe = Recipe.objects.get(slug=slug)
        
        if request.method == 'GET':
            # Get pagination params
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 20))
            
            # Validate pagination
            if page < 1:
                page = 1
            if limit < 1 or limit > 100:
                limit = 20
            
            # Calculate offset
            offset = (page - 1) * limit
            
            # Get comments
            total_comments = Comment.objects(recipe=recipe).count()
            comments = Comment.objects(recipe=recipe).order_by('-created_at').skip(offset).limit(limit)
            
            # Convert to dict
            current_user = request.user if request.user.is_authenticated else None
            comments_data = [comment.to_dict(current_user=current_user) for comment in comments]
            
            # Calculate pagination info
            total_pages = (total_comments + limit - 1) // limit  # Ceiling division
            has_next = page < total_pages
            has_prev = page > 1
            
            return Response({
                'comments': comments_data,
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': total_comments,
                    'total_pages': total_pages,
                    'has_next': has_next,
                    'has_prev': has_prev
                }
            }, status=status.HTTP_200_OK)
        
        elif request.method == 'POST':
            # Require authentication for POST
            if not request.user.is_authenticated:
                return Response(
                    {'error': 'Authentication required'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Get content from request
            content = request.data.get('content', '').strip()
            
            # Validate content
            if not content:
                return Response(
                    {'error': 'Comment content is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if len(content) > 2000:
                return Response(
                    {'error': 'Comment is too long (max 2000 characters)'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create comment
            comment = Comment(
                user=request.user,
                recipe=recipe,
                content=content
            )
            comment.save()
            
            # Track action and award XP
            xp_result = track_comment_posted(request.user, recipe)
            
            # Check for badge achievements
            badges_earned = check_and_award_badges(request.user)
            
            # Send notification to recipe author
            try:
                from .notification_helpers import notify_new_comment
                notify_new_comment(recipe.author, request.user, recipe, comment)
            except Exception as e:
                pass  # Don't fail if notification fails
            
            # Extract serializable data from xp_result
            xp_awarded = 0
            level_up_info = None
            if xp_result and xp_result.get('action'):
                xp_awarded = xp_result['action'].xp_awarded
            if xp_result and xp_result.get('xp_result'):
                level_up_info = xp_result['xp_result']
            
            return Response({
                'comment': comment.to_dict(current_user=request.user),
                'xp_awarded': xp_awarded,
                'level_up': level_up_info,
                'badges_earned': badges_earned
            }, status=status.HTTP_201_CREATED)
    
    except Recipe.DoesNotExist:
        return Response(
            {'error': 'Recipe not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except ValueError as e:
        return Response(
            {'error': 'Invalid pagination parameters'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_comment(request, comment_id):
    """
    Update a comment (only by the comment author)
    PUT /api/comments/:id/
    Body: { "content": "updated text" }
    """
    try:
        # Get comment
        comment = Comment.objects.get(id=comment_id)
        
        # Check if user is the author
        if str(comment.user.id) != str(request.user.id):
            return Response(
                {'error': 'You can only edit your own comments'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get new content
        content = request.data.get('content', '').strip()
        
        # Validate content
        if not content:
            return Response(
                {'error': 'Comment content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(content) > 2000:
            return Response(
                {'error': 'Comment is too long (max 2000 characters)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update comment
        comment.content = content
        comment.updated_at = datetime.utcnow()
        comment.is_edited = True
        comment.save()
        
        return Response({
            'comment': comment.to_dict(current_user=request.user),
            'message': 'Comment updated successfully'
        }, status=status.HTTP_200_OK)
    
    except Comment.DoesNotExist:
        return Response(
            {'error': 'Comment not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    """
    Delete a comment (only by the comment author)
    DELETE /api/comments/:id/
    """
    try:
        # Get comment
        comment = Comment.objects.get(id=comment_id)
        
        # Check if user is the author
        if str(comment.user.id) != str(request.user.id):
            return Response(
                {'error': 'You can only delete your own comments'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Delete comment
        comment.delete()
        
        return Response({
            'message': 'Comment deleted successfully'
        }, status=status.HTTP_200_OK)
    
    except Comment.DoesNotExist:
        return Response(
            {'error': 'Comment not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_comment_like(request, comment_id):
    """
    Toggle like on a comment
    POST /api/comments/:id/like/
    """
    try:
        # Get comment
        comment = Comment.objects.get(id=comment_id)
        
        # Check if user already liked
        user_liked = any(str(like.id) == str(request.user.id) for like in comment.likes)
        
        if user_liked:
            # Unlike - remove user from likes
            comment.likes = [like for like in comment.likes if str(like.id) != str(request.user.id)]
            action = 'unliked'
        else:
            # Like - add user to likes
            comment.likes.append(request.user)
            action = 'liked'
            
            # Send notification to comment author
            try:
                from .notification_helpers import notify_comment_like
                notify_comment_like(comment.user, request.user, comment)
            except Exception as e:
                pass  # Don't fail if notification fails
        
        comment.save()
        
        return Response({
            'action': action,
            'likes_count': len(comment.likes),
            'comment': comment.to_dict(current_user=request.user)
        }, status=status.HTTP_200_OK)
    
    except Comment.DoesNotExist:
        return Response(
            {'error': 'Comment not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
