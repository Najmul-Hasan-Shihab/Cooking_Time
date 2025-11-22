"""
API endpoints for saved recipes functionality
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from mongoengine import DoesNotExist, NotUniqueError
from mongoengine import Document, ReferenceField, DateTimeField
from datetime import datetime
from apps.recipes.models import Recipe
from apps.users.models import User


class SavedRecipe(Document):
    """Track saved recipes for users"""
    
    user = ReferenceField(User, required=True)
    recipe = ReferenceField(Recipe, required=True)
    saved_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'saved_recipes',
        'indexes': [
            'user',
            'recipe',
            {'fields': ['user', 'recipe'], 'unique': True}  # Prevent duplicate saves
        ]
    }
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'recipe': self.recipe.to_dict() if self.recipe else None,
            'saved_at': self.saved_at.isoformat() if self.saved_at else None
        }


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_save_recipe(request, slug):
    """
    Toggle save/unsave a recipe
    POST /api/recipes/{slug}/save/
    """
    try:
        # Get the recipe
        recipe = Recipe.objects.get(slug=slug)
        
        # Check if already saved
        existing_save = SavedRecipe.objects(user=request.user.id, recipe=recipe).first()
        
        if existing_save:
            # Unsave
            existing_save.delete()
            return Response({
                'message': 'Recipe removed from saved list',
                'is_saved': False
            })
        else:
            # Save
            saved_recipe = SavedRecipe(
                user=request.user.id,
                recipe=recipe
            )
            saved_recipe.save()
            
            return Response({
                'message': 'Recipe saved successfully!',
                'is_saved': True
            })
            
    except DoesNotExist:
        return Response(
            {'error': 'Recipe not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_saved_recipes(request):
    """
    Get user's saved recipes
    GET /api/recipes/saved/
    """
    try:
        saved_recipes = SavedRecipe.objects(user=request.user.id).order_by('-saved_at')
        
        results = []
        for saved in saved_recipes:
            recipe_data = saved.recipe.to_dict() if saved.recipe else None
            if recipe_data:
                recipe_data['saved_at'] = saved.saved_at.isoformat() if saved.saved_at else None
                results.append(recipe_data)
        
        return Response({
            'count': len(results),
            'results': results
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_cooked_recipes(request):
    """
    Get user's cooked recipes
    GET /api/recipes/cooked/
    """
    try:
        from apps.gamification.models import CookedRecipe
        
        cooked_recipes = CookedRecipe.objects(user=request.user.id).order_by('-cooked_at')
        
        results = []
        for cooked in cooked_recipes:
            recipe_data = cooked.recipe.to_dict() if cooked.recipe else None
            if recipe_data:
                recipe_data['cooked_at'] = cooked.cooked_at.isoformat() if cooked.cooked_at else None
                recipe_data['user_rating'] = cooked.rating
                recipe_data['user_notes'] = cooked.notes
                results.append(recipe_data)
        
        return Response({
            'count': len(results),
            'results': results
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
