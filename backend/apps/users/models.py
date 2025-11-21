"""
User model for MongoDB using MongoEngine
"""
from mongoengine import (
    Document, StringField, EmailField, ListField, 
    ReferenceField, IntField, DictField, DateTimeField, BooleanField
)
from datetime import datetime
import bcrypt


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
    badges = ListField(ReferenceField('Badge'))
    
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
        """Calculate user level based on XP"""
        # Level thresholds: 0, 100, 300, 600, 1000, 1500...
        thresholds = [0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500]
        
        for level, threshold in enumerate(thresholds, start=1):
            if self.xp < threshold:
                return level - 1
        
        # For XP beyond thresholds, use formula
        return 10 + ((self.xp - 4500) // 1000)
    
    def add_xp(self, amount):
        """Add XP and recalculate level"""
        self.xp += amount
        self.level = self.calculate_level()
        self.updated_at = datetime.utcnow()
    
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
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            'xp': self.xp,
            'level': self.level,
            'badges': [str(badge.id) for badge in self.badges] if self.badges else [],
            'followers_count': len(self.followers) if self.followers else 0,
            'following_count': len(self.following) if self.following else 0,
            'preferences': self.preferences,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __str__(self):
        return f"User: {self.username}"
