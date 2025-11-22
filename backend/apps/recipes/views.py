"""
Recipe Views - CRUD operations and actions
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from apps.recipes.models import Recipe, Comment
from apps.users.models import User
from apps.users.gamification import award_xp_for_action
from .serializers import (
    RecipeListSerializer,
    RecipeDetailSerializer,
    RecipeCreateUpdateSerializer,
    CommentSerializer
)


class RecipePagination(PageNumberPagination):
    """Custom pagination for recipes"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def recipe_list_create(request):
    """
    GET: List all published recipes with filters
    POST: Create new recipe (auth required)
    """
    if request.method == 'GET':
        # Build query
        query = {'is_published': True}
        
        # Filters
        author_id = request.query_params.get('author')
        if author_id:
            try:
                author = User.objects(id=author_id).first()
                if author:
                    query['author'] = author
            except:
                pass
        
        tags = request.query_params.getlist('tags')
        if tags:
            query['tags__in'] = tags
        
        difficulty = request.query_params.get('difficulty')
        if difficulty:
            query['difficulty'] = difficulty
        
        cuisine = request.query_params.get('cuisine')
        if cuisine:
            query['cuisine__icontains'] = cuisine
        
        # Dietary restrictions filter
        dietary = request.query_params.getlist('dietary_restrictions')
        if dietary:
            query['dietary_restrictions__all'] = dietary
        
        # Rarity filter
        rarity = request.query_params.get('rarity')
        if rarity and rarity in ['common', 'rare', 'epic', 'legendary']:
            query['rarity'] = rarity
        
        # Time range filters
        time_min = request.query_params.get('time_min')
        time_max = request.query_params.get('time_max')
        
        # Ingredient search
        ingredient_search = request.query_params.get('ingredient')
        
        # Get initial recipes
        recipes = Recipe.objects(**query)
        
        # Filter by time range (need to compute total_time)
        if time_min or time_max:
            filtered_recipes = []
            for r in recipes:
                total = r.total_time
                if time_min and total < int(time_min):
                    continue
                if time_max and total > int(time_max):
                    continue
                filtered_recipes.append(r)
            recipes = filtered_recipes
        
        # Filter by ingredient
        if ingredient_search:
            ingredient_lower = ingredient_search.lower()
            recipes = [r for r in recipes if any(ingredient_lower in ing.name.lower() for ing in r.ingredients)]
        
        # Search by title
        search = request.query_params.get('q')
        if search:
            search_lower = search.lower()
            recipes = [r for r in recipes if search_lower in r.title.lower()]
        
        # Sorting
        sort_by = request.query_params.get('sort', '-created_at')
        allowed_sorts = ['created_at', '-created_at', 'views', '-views', 'rating_stats.average', '-rating_stats.average']
        if sort_by not in allowed_sorts:
            sort_by = '-created_at'
        
        # Apply sorting if we filtered manually
        if time_min or time_max or ingredient_search or search:
            # Already have a list, sort it
            reverse = sort_by.startswith('-')
            sort_field = sort_by.lstrip('-')
            
            if sort_field == 'rating_stats.average':
                recipes = sorted(recipes, key=lambda r: r.rating_stats.average if r.rating_stats else 0, reverse=reverse)
            elif sort_field == 'views':
                recipes = sorted(recipes, key=lambda r: r.views, reverse=reverse)
            elif sort_field == 'created_at':
                recipes = sorted(recipes, key=lambda r: r.created_at, reverse=reverse)
        else:
            # Use database sorting
            recipes = recipes.order_by(sort_by)
        
        # Paginate
        paginator = RecipePagination()
        page = paginator.paginate_queryset(list(recipes), request)
        serializer = RecipeListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        # Create recipe (requires authentication)
        if not hasattr(request, 'user_id'):
            return Response({
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = RecipeCreateUpdateSerializer(
            data=request.data,
            context={'author_id': request.user_id}
        )
        
        if serializer.is_valid():
            recipe = serializer.save()
            
            # Award XP for submitting recipe
            author = User.objects(id=request.user_id).first()
            if author:
                award_xp_for_action(
                    user=author,
                    action_type='submit_recipe',
                    target_id=str(recipe.id)
                )
            
            return Response(
                RecipeDetailSerializer(recipe).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def recipe_detail(request, slug):
    """
    GET: Get recipe detail
    PUT/PATCH: Update recipe (author only)
    DELETE: Delete recipe (author or admin)
    """
    recipe = Recipe.objects(slug=slug).first()
    
    if not recipe:
        return Response({
            'error': 'Recipe not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        # Increment view count
        recipe.add_view()
        
        serializer = RecipeDetailSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method in ['PUT', 'PATCH']:
        # Update recipe (requires authentication and ownership)
        if not hasattr(request, 'user_id'):
            return Response({
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if str(recipe.author.id) != request.user_id:
            user = User.objects(id=request.user_id).first()
            if not user or not user.is_admin:
                return Response({
                    'error': 'Permission denied'
                }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = RecipeCreateUpdateSerializer(
            recipe,
            data=request.data,
            partial=(request.method == 'PATCH'),
            context={'author_id': request.user_id}
        )
        
        if serializer.is_valid():
            recipe = serializer.save()
            return Response(
                RecipeDetailSerializer(recipe).data,
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Delete recipe (requires admin)
        if not hasattr(request, 'user_id'):
            return Response({
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        user = User.objects(id=request.user_id).first()
        if not user or not user.is_admin:
            return Response({
                'error': 'Admin permission required'
            }, status=status.HTTP_403_FORBIDDEN)
        
        recipe.delete()
        return Response({
            'message': 'Recipe deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_cooked(request, slug):
    """Mark recipe as cooked and award XP"""
    if not hasattr(request, 'user_id'):
        return Response({
            'error': 'Authentication required'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    recipe = Recipe.objects(slug=slug).first()
    if not recipe:
        return Response({
            'error': 'Recipe not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Increment cook count
    recipe.add_cook()
    
    # Award XP to user
    user = User.objects(id=request.user_id).first()
    if user:
        user_action = award_xp_for_action(
            user=user,
            action_type='cook',
            target_id=str(recipe.id),
            metadata={'recipe_title': recipe.title}
        )
        
        return Response({
            'message': 'Recipe marked as cooked',
            'xp_awarded': user_action.xp_awarded,
            'user': {
                'xp': user.xp,
                'level': user.level
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'User not found'
    }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_recipes(request):
    """Advanced recipe search"""
    query = request.query_params.get('q', '')
    
    if not query:
        return Response({
            'error': 'Search query required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Search in title, description, tags, and ingredients
    recipes = Recipe.objects(
        is_published=True
    ).filter(
        title__icontains=query
    ) | Recipe.objects(
        is_published=True
    ).filter(
        description__icontains=query
    ) | Recipe.objects(
        is_published=True,
        tags__icontains=query
    )
    
    # Paginate results
    paginator = RecipePagination()
    page = paginator.paginate_queryset(list(recipes), request)
    serializer = RecipeListSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_cooked(request, slug):
    """
    Mark a recipe as cooked by the current user
    POST /api/recipes/:slug/mark_cooked/
    
    Body (all optional):
    {
        "photo_url": "https://...",
        "rating": 4.5,
        "notes": "Turned out great!"
    }
    
    Returns:
    {
        "message": "Recipe marked as cooked!",
        "xp_result": {...},
        "badges_earned": [...],
        "cooked_recipe": {...}
    }
    """
    try:
        from apps.gamification.models import CookedRecipe
        from apps.gamification.action_tracker import track_recipe_cooked
        from apps.gamification.badge_engine import check_and_award_badges
        
        # Get recipe
        recipe = Recipe.objects.get(slug=slug, is_published=True)
        user = request.user
        
        # Get optional data
        photo_url = request.data.get('photo_url')
        rating = request.data.get('rating')
        notes = request.data.get('notes')
        
        # Validate rating if provided
        if rating is not None:
            try:
                rating = float(rating)
                if rating < 1.0 or rating > 5.0:
                    return Response({
                        'error': 'Rating must be between 1.0 and 5.0'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except (ValueError, TypeError):
                return Response({
                    'error': 'Invalid rating value'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already cooked this recipe
        existing = CookedRecipe.objects(user=user, recipe=recipe).first()
        if existing:
            return Response({
                'error': 'You have already marked this recipe as cooked',
                'cooked_at': existing.cooked_at.isoformat() if existing.cooked_at else None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create cooked recipe record
        cooked_recipe = CookedRecipe(
            user=user,
            recipe=recipe,
            photo_url=photo_url,
            rating=rating,
            notes=notes
        )
        cooked_recipe.save()
        
        # Increment cook count
        recipe.cook_count += 1
        recipe.save()
        
        # Track action and award XP
        has_photo = bool(photo_url)
        has_rating = rating is not None
        action_result = track_recipe_cooked(user, recipe, has_photo=has_photo, has_rating=has_rating)
        
        # Check for new badges
        badges_earned = []
        if action_result['success']:
            badges_earned = check_and_award_badges(user)
        
        # Send notification to recipe author
        try:
            from apps.gamification.notification_helpers import notify_recipe_cooked
            notify_recipe_cooked(recipe.author, user, recipe)
        except Exception as e:
            pass  # Don't fail if notification fails
        
        # Update recipe rating if rating was provided
        if rating:
            recipe.rating_stats.count += 1
            recipe.rating_stats.total += rating
            recipe.rating_stats.average = recipe.rating_stats.total / recipe.rating_stats.count
            recipe.save()
        
        return Response({
            'message': 'Recipe marked as cooked!',
            'xp_result': action_result.get('xp_result'),
            'badges_earned': badges_earned,
            'cooked_recipe': cooked_recipe.to_dict(),
            'recipe': {
                'slug': recipe.slug,
                'title': recipe.title,
                'cook_count': recipe.cook_count,
                'rating_stats': {
                    'average': recipe.rating_stats.average,
                    'count': recipe.rating_stats.count
                }
            }
        }, status=status.HTTP_201_CREATED)
        
    except Recipe.DoesNotExist:
        return Response({
            'error': 'Recipe not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
