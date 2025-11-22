"""
User model for MongoDB using MongoEngine
"""
from mongoengine import (
    Document, StringField, EmailField, ListField, 
    ReferenceField, IntField, DictField, DateTimeField, BooleanField
)
from datetime import datetime
import bcrypt
import sys
import os

# Add the gamification app to path for importing xp_system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gamification.xp_system import (
    calculate_level_from_xp, 
    get_xp_for_next_level,
    check_level_up,
    get_level_name
)


class User(Document):
    """User document for authentication and profile"""
    
    # Basic Info
    username = StringField(required=True, unique=True, max_length=50)
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)
    
    # Profile
    avatar_url = StringField(max_length=500)
    bio = StringField(max_length=500)
    
    # Gamification
    xp = IntField(default=0)
    level = IntField(default=1)
    badges = ListField(StringField())  # Store badge IDs as strings
    
    # Social
    followers = ListField(ReferenceField('self'))
    following = ListField(ReferenceField('self'))
    
    # Preferences
    preferences = DictField(default={
        'cuisines': [],
        'dietary_restrictions': [],
        'favorite_tags': []
    })
    
    # Metadata
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=True)
    is_admin = BooleanField(default=False)
    
    meta = {
        'collection': 'users',
        'indexes': [
            'username',
            'email',
            '-created_at',
            '-xp'
        ]
    }
    
    def set_password(self, password):
        """Hash and set user password"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Verify password against hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            self.password_hash.encode('utf-8')
        )
    
    def calculate_level(self):
        """Calculate user level based on XP using the new XP system"""
        return calculate_level_from_xp(self.xp)
    
    def add_xp(self, amount, action_type=None):
        """
        Add XP and recalculate level
        
        Args:
            amount (int): XP points to add
            action_type (str, optional): Type of action that triggered XP gain
            
        Returns:
            dict: {
                'xp_gained': int,
                'new_xp': int,
                'new_level': int,
                'level_up': dict or None (if leveled up)
            }
        """
        old_xp = self.xp
        old_level = self.level
        
        self.xp += amount
        self.level = self.calculate_level()
        self.updated_at = datetime.utcnow()
        
        # Check if user leveled up
        level_up_info = check_level_up(old_xp, self.xp)
        
        # Send level-up notification
        if level_up_info and self.level > old_level:
            try:
                from apps.gamification.notification_helpers import notify_level_up
                notify_level_up(self, self.level)
            except Exception as e:
                pass  # Don't fail if notification fails
        
        return {
            'xp_gained': amount,
            'new_xp': self.xp,
            'old_level': old_level,
            'new_level': self.level,
            'level_up': level_up_info,
            'action_type': action_type
        }
    
    def get_xp_progress(self):
        """Get detailed XP progress information"""
        return get_xp_for_next_level(self.xp)
    
    def get_level_title(self):
        """Get descriptive level name"""
        return get_level_name(self.level)
    
    @property
    def is_authenticated(self):
        """Always return True for authenticated users (required by Django REST Framework)"""
        return True
    
    @property
    def is_anonymous(self):
        """Always return False for authenticated users"""
        return False
    
    def to_dict(self):
        """Convert user to dictionary (for API responses)"""
        xp_progress = self.get_xp_progress()
        
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            'xp': self.xp,
            'level': self.level,
            'level_title': self.get_level_title(),
            'xp_progress': xp_progress,
            'badges': self.badges if self.badges else [],
            'followers_count': len(self.followers) if self.followers else 0,
            'following_count': len(self.following) if self.following else 0,
            'preferences': self.preferences,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __str__(self):
        return f"User: {self.username}"
