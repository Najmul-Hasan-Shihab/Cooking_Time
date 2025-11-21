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
        tags = request.query_params.getlist('tags')
        if tags:
            query['tags__in'] = tags
        
        difficulty = request.query_params.get('difficulty')
        if difficulty:
            query['difficulty'] = difficulty
        
        cuisine = request.query_params.get('cuisine')
        if cuisine:
            query['cuisine__icontains'] = cuisine
        
        time_max = request.query_params.get('time_max')
        if time_max:
            # Filter by total time
            recipes = Recipe.objects(**query)
            recipes = [r for r in recipes if r.total_time <= int(time_max)]
            
            # Paginate
            paginator = RecipePagination()
            page = paginator.paginate_queryset(recipes, request)
            serializer = RecipeListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # Search
        search = request.query_params.get('q')
        if search:
            query['title__icontains'] = search
        
        # Sorting
        sort_by = request.query_params.get('sort', '-created_at')
        allowed_sorts = ['created_at', '-created_at', 'views', '-views', 'rating_stats.average', '-rating_stats.average']
        if sort_by not in allowed_sorts:
            sort_by = '-created_at'
        
        # Get recipes
        recipes = Recipe.objects(**query).order_by(sort_by)
        
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
