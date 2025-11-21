"""
Recipe and related models for MongoDB using MongoEngine
"""
from mongoengine import (
    Document, StringField, IntField, FloatField, ListField,
    EmbeddedDocument, EmbeddedDocumentField, ReferenceField,
    DateTimeField, DictField, BooleanField
)
from datetime import datetime
from slugify import slugify


class Ingredient(EmbeddedDocument):
    """Embedded document for recipe ingredients"""
    name = StringField(required=True, max_length=100)
    quantity = StringField(max_length=50)
    unit = StringField(max_length=50)
    optional = BooleanField(default=False)


class RecipeStep(EmbeddedDocument):
    """Embedded document for recipe steps"""
    step_number = IntField(required=True)
    text = StringField(required=True)
    image = StringField(max_length=500)
    step_time = IntField()  # in minutes


class NutritionInfo(EmbeddedDocument):
    """Embedded document for nutrition information"""
    calories = IntField()
    protein = FloatField()
    carbs = FloatField()
    fat = FloatField()
    fiber = FloatField()
    sugar = FloatField()


class RatingStats(EmbeddedDocument):
    """Embedded document for rating statistics"""
    average = FloatField(default=0.0)
    count = IntField(default=0)
    total = IntField(default=0)


class Recipe(Document):
    """Recipe document"""
    
    # Basic Info
    title = StringField(required=True, max_length=200)
    slug = StringField(required=True, unique=True)
    description = StringField(max_length=1000)
    author = ReferenceField('User', required=True)
    
    # Media
    images = ListField(StringField(max_length=500))
    
    # Recipe Content
    ingredients = ListField(EmbeddedDocumentField(Ingredient))
    steps = ListField(EmbeddedDocumentField(RecipeStep))
    
    # Metadata
    prep_time = IntField()  # in minutes
    cook_time = IntField()  # in minutes
    servings = IntField(default=1)
    difficulty = StringField(
        choices=['easy', 'medium', 'hard'],
        default='medium'
    )
    
    # Classification
    tags = ListField(StringField(max_length=50))
    categories = ListField(StringField(max_length=50))
    cuisine = StringField(max_length=100)
    
    # Nutrition (optional)
    nutrition = EmbeddedDocumentField(NutritionInfo)
    
    # Stats
    rating_stats = EmbeddedDocumentField(RatingStats, default=RatingStats)
    views = IntField(default=0)
    cook_count = IntField(default=0)  # How many times marked as cooked
    
    # Gamification
    rarity = StringField(
        choices=['common', 'rare', 'epic', 'legendary'],
        default='common'
    )
    
    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    # Moderation
    is_published = BooleanField(default=False)
    is_featured = BooleanField(default=False)
    
    meta = {
        'collection': 'recipes',
        'indexes': [
            'slug',
            'author',
            'tags',
            'difficulty',
            'cuisine',
            '-created_at',
            '-views',
            '-rating_stats.average',
            'is_published'
        ]
    }
    
    def save(self, *args, **kwargs):
        """Override save to auto-generate slug"""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            
            # Ensure unique slug
            while Recipe.objects(slug=slug).first():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        self.updated_at = datetime.utcnow()
        return super(Recipe, self).save(*args, **kwargs)
    
    @property
    def total_time(self):
        """Calculate total cooking time"""
        prep = self.prep_time or 0
        cook = self.cook_time or 0
        return prep + cook
    
    def calculate_rarity(self):
        """Calculate recipe rarity based on various factors"""
        score = 0
        
        # More ingredients = rarer
        if len(self.ingredients) > 15:
            score += 2
        elif len(self.ingredients) > 10:
            score += 1
        
        # Longer cook time = rarer
        if self.total_time > 120:
            score += 2
        elif self.total_time > 60:
            score += 1
        
        # High rating = rarer
        if self.rating_stats.average >= 4.5:
            score += 2
        elif self.rating_stats.average >= 4.0:
            score += 1
        
        # Determine rarity
        if score >= 5:
            return 'legendary'
        elif score >= 3:
            return 'epic'
        elif score >= 2:
            return 'rare'
        else:
            return 'common'
    
    def add_view(self):
        """Increment view count"""
        self.views += 1
        self.save()
    
    def add_cook(self):
        """Increment cook count"""
        self.cook_count += 1
        self.save()
    
    def to_dict(self, include_author=True):
        """Convert recipe to dictionary"""
        data = {
            'id': str(self.id),
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'images': self.images,
            'ingredients': [
                {
                    'name': ing.name,
                    'quantity': ing.quantity,
                    'unit': ing.unit,
                    'optional': ing.optional
                } for ing in self.ingredients
            ] if self.ingredients else [],
            'steps': [
                {
                    'step_number': step.step_number,
                    'text': step.text,
                    'image': step.image,
                    'step_time': step.step_time
                } for step in self.steps
            ] if self.steps else [],
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'total_time': self.total_time,
            'servings': self.servings,
            'difficulty': self.difficulty,
            'tags': self.tags,
            'categories': self.categories,
            'cuisine': self.cuisine,
            'rating_stats': {
                'average': self.rating_stats.average if self.rating_stats else 0.0,
                'count': self.rating_stats.count if self.rating_stats else 0,
            },
            'views': self.views,
            'cook_count': self.cook_count,
            'rarity': self.rarity,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_published': self.is_published,
            'is_featured': self.is_featured,
        }
        
        if include_author and self.author:
            data['author'] = {
                'id': str(self.author.id),
                'username': self.author.username,
                'avatar_url': self.author.avatar_url,
                'level': self.author.level,
            }
        
        if self.nutrition:
            data['nutrition'] = {
                'calories': self.nutrition.calories,
                'protein': self.nutrition.protein,
                'carbs': self.nutrition.carbs,
                'fat': self.nutrition.fat,
            }
        
        return data
    
    def __str__(self):
        return f"Recipe: {self.title}"


class Comment(Document):
    """Comment document for recipes"""
    recipe = ReferenceField(Recipe, required=True)
    user = ReferenceField('User', required=True)
    text = StringField(required=True, max_length=1000)
    parent = ReferenceField('self')  # For threading
    likes = IntField(default=0)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    is_edited = BooleanField(default=False)
    
    meta = {
        'collection': 'comments',
        'indexes': [
            'recipe',
            'user',
            'parent',
            '-created_at'
        ]
    }
    
    def to_dict(self):
        """Convert comment to dictionary"""
        return {
            'id': str(self.id),
            'recipe_id': str(self.recipe.id),
            'user': {
                'id': str(self.user.id),
                'username': self.user.username,
                'avatar_url': self.user.avatar_url,
            },
            'text': self.text,
            'parent_id': str(self.parent.id) if self.parent else None,
            'likes': self.likes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_edited': self.is_edited,
        }
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.title}"
