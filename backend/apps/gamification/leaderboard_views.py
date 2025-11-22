"""
Leaderboard API endpoints
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User
from apps.recipes.models import Recipe
from apps.gamification.models import CookedRecipe
from datetime import datetime, timedelta


@api_view(['GET'])
def leaderboard_by_xp(request):
    """
    Get leaderboard ranked by XP
    GET /api/leaderboard/xp/?timeframe=all&page=1&limit=50
    
    Timeframe options: all, week, month, year
    """
    try:
        timeframe = request.GET.get('timeframe', 'all')
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 50)), 100)  # Max 100
        
        # Get all users ordered by XP
        users = User.objects.all().order_by('-xp')
        
        # Filter by timeframe if needed
        if timeframe != 'all':
            cutoff_date = get_cutoff_date(timeframe)
            if cutoff_date:
                # For timeframe filtering, we'd need to track XP changes over time
                # For now, just return all-time rankings
                pass
        
        # Pagination
        start = (page - 1) * limit
        end = start + limit
        total = users.count()
        
        results = []
        for idx, user in enumerate(users[start:end], start=start + 1):
            results.append({
                'rank': idx,
                'user': {
                    'id': str(user.id),
                    'username': user.username,
                    'level': user.level,
                    'xp': user.xp,
                },
                'stats': {
                    'recipes_created': Recipe.objects(author=user, is_published=True).count(),
                    'recipes_cooked': CookedRecipe.objects(user=user).count(),
                }
            })
        
        return Response({
            'count': total,
            'page': page,
            'limit': limit,
            'total_pages': (total + limit - 1) // limit,
            'results': results
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def leaderboard_by_recipes(request):
    """
    Get leaderboard ranked by recipes created
    GET /api/leaderboard/recipes/?page=1&limit=50
    """
    try:
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 50)), 100)
        
        # Get all users
        all_users = User.objects.all()
        
        # Count recipes for each user and sort
        user_data = []
        for user in all_users:
            recipe_count = Recipe.objects(author=user, is_published=True).count()
            if recipe_count > 0:  # Only include users with recipes
                user_data.append({
                    'user': user,
                    'recipe_count': recipe_count
                })
        
        # Sort by recipe count
        user_data.sort(key=lambda x: x['recipe_count'], reverse=True)
        
        # Pagination
        total = len(user_data)
        start = (page - 1) * limit
        end = start + limit
        
        results = []
        for idx, data in enumerate(user_data[start:end], start=start + 1):
            user = data['user']
            results.append({
                'rank': idx,
                'user': {
                    'id': str(user.id),
                    'username': user.username,
                    'level': user.level,
                    'xp': user.xp,
                },
                'stats': {
                    'recipes_created': data['recipe_count'],
                    'recipes_cooked': CookedRecipe.objects(user=user).count(),
                }
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


@api_view(['GET'])
def leaderboard_by_cooked(request):
    """
    Get leaderboard ranked by recipes cooked
    GET /api/leaderboard/cooked/?page=1&limit=50
    """
    try:
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 50)), 100)
        
        # Get all users
        all_users = User.objects.all()
        
        # Count cooked recipes for each user and sort
        user_data = []
        for user in all_users:
            cooked_count = CookedRecipe.objects(user=user).count()
            if cooked_count > 0:  # Only include users who cooked recipes
                user_data.append({
                    'user': user,
                    'cooked_count': cooked_count
                })
        
        # Sort by cooked count
        user_data.sort(key=lambda x: x['cooked_count'], reverse=True)
        
        # Pagination
        total = len(user_data)
        start = (page - 1) * limit
        end = start + limit
        
        results = []
        for idx, data in enumerate(user_data[start:end], start=start + 1):
            user = data['user']
            results.append({
                'rank': idx,
                'user': {
                    'id': str(user.id),
                    'username': user.username,
                    'level': user.level,
                    'xp': user.xp,
                },
                'stats': {
                    'recipes_created': Recipe.objects(author=user, is_published=True).count(),
                    'recipes_cooked': data['cooked_count'],
                }
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


def get_cutoff_date(timeframe):
    """Get cutoff date for timeframe filtering"""
    now = datetime.utcnow()
    if timeframe == 'week':
        return now - timedelta(days=7)
    elif timeframe == 'month':
        return now - timedelta(days=30)
    elif timeframe == 'year':
        return now - timedelta(days=365)
    return None
