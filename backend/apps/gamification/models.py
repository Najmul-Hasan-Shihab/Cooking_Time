"""
Gamification models for badges, user actions, and cooked recipes
"""
from mongoengine import (
    Document, StringField, IntField, ReferenceField,
    DateTimeField, FloatField, BooleanField, ListField
)
from datetime import datetime


class Badge(Document):
    """Badge/Achievement document"""
    
    name = StringField(required=True, unique=True, max_length=100)
    description = StringField(required=True, max_length=500)
    icon = StringField(required=True, max_length=10)  # Emoji or icon code
    criteria_type = StringField(required=True, choices=[
        'recipes_created',
        'recipes_cooked',
        'total_xp',
        'level_reached',
        'followers',
        'likes_received',
        'comments_posted',
        'special'  # Manually awarded
    ])
    criteria_value = IntField(required=True)  # Threshold to earn badge
    rarity = StringField(required=True, choices=['common', 'rare', 'epic', 'legendary'], default='common')
    xp_reward = IntField(default=0)  # Bonus XP for earning this badge
    
    created_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=True)
    
    meta = {
        'collection': 'badges',
        'indexes': ['criteria_type', 'rarity']
    }
    
    def to_dict(self):
        """Convert badge to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'criteria_type': self.criteria_type,
            'criteria_value': self.criteria_value,
            'rarity': self.rarity,
            'xp_reward': self.xp_reward,
        }
    
    def __str__(self):
        return f"{self.name} ({self.rarity})"


class UserAction(Document):
    """Track user actions for XP and analytics"""
    
    user = ReferenceField('User', required=True)
    action_type = StringField(required=True, choices=[
        'recipe_created',
        'recipe_cooked',
        'photo_uploaded',
        'recipe_rated',
        'comment_posted',
        'recipe_liked',
        'user_followed',
        'daily_login',
        'badge_earned'
    ])
    target_recipe = ReferenceField('Recipe', null=True)  # If action is recipe-related
    xp_awarded = IntField(default=0)
    metadata = StringField(max_length=500, null=True)  # JSON string for additional data
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'user_actions',
        'indexes': [
            'user',
            'action_type',
            '-created_at',
            ('user', '-created_at')
        ]
    }
    
    def to_dict(self):
        """Convert action to dictionary"""
        return {
            'id': str(self.id),
            'user_id': str(self.user.id),
            'action_type': self.action_type,
            'target_recipe_id': str(self.target_recipe.id) if self.target_recipe else None,
            'xp_awarded': self.xp_awarded,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __str__(self):
        return f"{self.user.username} - {self.action_type}"


class CookedRecipe(Document):
    """Track recipes that users have cooked"""
    
    user = ReferenceField('User', required=True)
    recipe = ReferenceField('Recipe', required=True)
    photo_url = StringField(max_length=500, null=True)
    rating = FloatField(min_value=1.0, max_value=5.0, null=True)
    notes = StringField(max_length=1000, null=True)
    cooked_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'cooked_recipes',
        'indexes': [
            'user',
            'recipe',
            '-cooked_at',
            ('user', 'recipe')  # Compound index for uniqueness check
        ]
    }
    
    def to_dict(self):
        """Convert cooked recipe to dictionary"""
        return {
            'id': str(self.id),
            'user_id': str(self.user.id),
            'recipe_id': str(self.recipe.id),
            'recipe_title': self.recipe.title if self.recipe else None,
            'photo_url': self.photo_url,
            'rating': self.rating,
            'notes': self.notes,
            'cooked_at': self.cooked_at.isoformat() if self.cooked_at else None,
        }
    
    def __str__(self):
        return f"{self.user.username} cooked {self.recipe.title}"


class Comment(Document):
    """Recipe comment/review document"""
    
    user = ReferenceField('User', required=True)
    recipe = ReferenceField('Recipe', required=True)
    content = StringField(required=True, max_length=2000)
    likes = ListField(ReferenceField('User'), default=list)  # Users who liked this comment
    
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    is_edited = BooleanField(default=False)
    
    meta = {
        'collection': 'comments',
        'indexes': [
            'user',
            'recipe',
            '-created_at',
            ('recipe', '-created_at')  # Compound index for recipe comments
        ]
    }
    
    def to_dict(self, current_user=None):
        """Convert comment to dictionary"""
        liked_by_current_user = False
        if current_user:
            liked_by_current_user = any(str(like.id) == str(current_user.id) for like in self.likes)
        
        return {
            'id': str(self.id),
            'author': {
                'id': str(self.user.id),
                'username': self.user.username,
                'avatar_url': self.user.avatar_url,
                'level': self.user.level if hasattr(self.user, 'level') else 1,
            },
            'recipe_id': str(self.recipe.id),
            'content': self.content,
            'likes_count': len(self.likes),
            'is_liked': liked_by_current_user,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_edited': self.is_edited,
        }
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.title}"
