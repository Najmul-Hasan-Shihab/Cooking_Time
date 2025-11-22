"""
Recipe Serializers
"""
from rest_framework import serializers
from apps.recipes.models import Recipe, Ingredient, RecipeStep, Comment
from apps.users.models import User


class IngredientSerializer(serializers.Serializer):
    """Serializer for ingredient embedded document"""
    name = serializers.CharField(max_length=100)
    quantity = serializers.CharField(max_length=50, required=False, allow_blank=True)
    unit = serializers.CharField(max_length=50, required=False, allow_blank=True)
    optional = serializers.BooleanField(default=False)


class RecipeStepSerializer(serializers.Serializer):
    """Serializer for recipe step embedded document"""
    step_number = serializers.IntegerField()
    text = serializers.CharField()
    image = serializers.URLField(required=False, allow_blank=True)
    step_time = serializers.IntegerField(required=False, allow_null=True)


class RecipeListSerializer(serializers.Serializer):
    """Serializer for recipe list (summary view)"""
    id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    slug = serializers.CharField(read_only=True)
    description = serializers.CharField()
    images = serializers.ListField(child=serializers.URLField(), required=False)
    difficulty = serializers.ChoiceField(choices=['easy', 'medium', 'hard'])
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    cuisine = serializers.CharField(required=False, allow_blank=True)
    dietary_restrictions = serializers.ListField(child=serializers.CharField(), required=False)
    prep_time = serializers.IntegerField(required=False, allow_null=True)
    cook_time = serializers.IntegerField(required=False, allow_null=True)
    servings = serializers.IntegerField(default=1)
    rating_stats = serializers.DictField(read_only=True)
    views = serializers.IntegerField(read_only=True)
    cook_count = serializers.IntegerField(read_only=True)
    rarity = serializers.CharField(read_only=True)
    author = serializers.DictField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(read_only=True)
    
    def to_representation(self, instance):
        """Convert Recipe document to dict"""
        if isinstance(instance, Recipe):
            return instance.to_dict()
        return instance


class RecipeDetailSerializer(RecipeListSerializer):
    """Serializer for recipe detail (full view)"""
    ingredients = IngredientSerializer(many=True, required=False)
    steps = RecipeStepSerializer(many=True, required=False)
    categories = serializers.ListField(child=serializers.CharField(), required=False)
    
    def to_representation(self, instance):
        """Convert Recipe document to dict"""
        if isinstance(instance, Recipe):
            return instance.to_dict(include_author=True)
        return instance


class RecipeCreateUpdateSerializer(serializers.Serializer):
    """Serializer for creating/updating recipes"""
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    images = serializers.ListField(
        child=serializers.URLField(),
        required=False,
        allow_empty=True
    )
    ingredients = IngredientSerializer(many=True, required=False, allow_empty=True)
    steps = RecipeStepSerializer(many=True, required=False, allow_empty=True)
    prep_time = serializers.IntegerField(required=False, allow_null=True, min_value=0)
    cook_time = serializers.IntegerField(required=False, allow_null=True, min_value=0)
    servings = serializers.IntegerField(default=1, min_value=1)
    difficulty = serializers.ChoiceField(
        choices=['easy', 'medium', 'hard'],
        default='medium'
    )
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        allow_empty=True
    )
    categories = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        allow_empty=True
    )
    cuisine = serializers.CharField(max_length=100, required=False, allow_blank=True)
    dietary_restrictions = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        allow_empty=True
    )
    
    def validate_ingredients(self, value):
        """Validate ingredients"""
        if value:
            for ing in value:
                if not ing.get('name'):
                    raise serializers.ValidationError("Each ingredient must have a name")
        return value
    
    def validate_steps(self, value):
        """Validate steps"""
        if value:
            step_numbers = [step.get('step_number') for step in value]
            if len(step_numbers) != len(set(step_numbers)):
                raise serializers.ValidationError("Step numbers must be unique")
        return value
    
    def create(self, validated_data):
        """Create new recipe"""
        ingredients_data = validated_data.pop('ingredients', [])
        steps_data = validated_data.pop('steps', [])
        
        # Get author from context
        author_id = self.context.get('author_id')
        author = User.objects(id=author_id).first()
        
        if not author:
            raise serializers.ValidationError("Author not found")
        
        # Create recipe
        recipe = Recipe(
            author=author,
            **validated_data
        )
        
        # Add ingredients
        recipe.ingredients = [Ingredient(**ing) for ing in ingredients_data]
        
        # Add steps
        recipe.steps = [RecipeStep(**step) for step in steps_data]
        
        # Calculate rarity
        recipe.rarity = recipe.calculate_rarity()
        
        recipe.save()
        return recipe
    
    def update(self, instance, validated_data):
        """Update existing recipe"""
        ingredients_data = validated_data.pop('ingredients', None)
        steps_data = validated_data.pop('steps', None)
        
        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update ingredients if provided
        if ingredients_data is not None:
            instance.ingredients = [Ingredient(**ing) for ing in ingredients_data]
        
        # Update steps if provided
        if steps_data is not None:
            instance.steps = [RecipeStep(**step) for step in steps_data]
        
        # Recalculate rarity
        instance.rarity = instance.calculate_rarity()
        
        instance.save()
        return instance


class CommentSerializer(serializers.Serializer):
    """Serializer for comments"""
    id = serializers.CharField(read_only=True)
    recipe_id = serializers.CharField(write_only=True, required=False)
    user = serializers.DictField(read_only=True)
    text = serializers.CharField(max_length=1000)
    parent_id = serializers.CharField(required=False, allow_null=True)
    likes = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    is_edited = serializers.BooleanField(read_only=True)
    
    def to_representation(self, instance):
        """Convert Comment document to dict"""
        if isinstance(instance, Comment):
            return instance.to_dict()
        return instance
