"""
Gamification models - Badges, User Actions, Challenges
"""
from mongoengine import (
    Document, StringField, IntField, ListField,
    ReferenceField, DateTimeField, DictField, BooleanField
)
from datetime import datetime


class Badge(Document):
    """Badge document for achievements"""
    name = StringField(required=True, unique=True, max_length=100)
    description = StringField(max_length=500)
    icon = StringField(max_length=500)  # URL or icon identifier
    criteria = DictField()  # Flexible criteria storage
    reward_xp = IntField(default=0)
    rarity = StringField(
        choices=['common', 'rare', 'epic', 'legendary'],
        default='common'
    )
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'badges',
        'indexes': ['name', 'rarity']
    }
    
    def to_dict(self):
        """Convert badge to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'reward_xp': self.reward_xp,
            'rarity': self.rarity,
        }
    
    def __str__(self):
        return f"Badge: {self.name}"


class UserAction(Document):
    """User action document for tracking gamification events"""
    user = ReferenceField('User', required=True)
    action_type = StringField(
        required=True,
        choices=[
            'submit_recipe',
            'cook',
            'comment',
            'share',
            'rate',
            'follow',
            'upload_photo'
        ]
    )
    target_id = StringField()  # ID of the target (recipe, comment, etc.)
    xp_awarded = IntField(default=0)
    metadata = DictField()  # Additional action data
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'user_actions',
        'indexes': [
            'user',
            'action_type',
            '-created_at'
        ]
    }
    
    def to_dict(self):
        """Convert user action to dictionary"""
        return {
            'id': str(self.id),
            'user_id': str(self.user.id),
            'action_type': self.action_type,
            'target_id': self.target_id,
            'xp_awarded': self.xp_awarded,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __str__(self):
        return f"{self.user.username} - {self.action_type}"


class Challenge(Document):
    """Challenge document for time-limited events"""
    title = StringField(required=True, max_length=200)
    description = StringField(max_length=1000)
    rules = DictField()  # Challenge rules and requirements
    reward_xp = IntField(default=0)
    reward_badge = ReferenceField(Badge)
    
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    
    participants = ListField(ReferenceField('User'))
    completers = ListField(ReferenceField('User'))
    
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'challenges',
        'indexes': [
            'start_date',
            'end_date',
            'is_active'
        ]
    }
    
    def is_ongoing(self):
        """Check if challenge is currently active"""
        now = datetime.utcnow()
        return self.start_date <= now <= self.end_date and self.is_active
    
    def add_participant(self, user):
        """Add user to challenge participants"""
        if user not in self.participants:
            self.participants.append(user)
            self.save()
    
    def complete_challenge(self, user):
        """Mark challenge as completed by user"""
        if user not in self.completers and user in self.participants:
            self.completers.append(user)
            
            # Award XP and badge
            user.add_xp(self.reward_xp)
            if self.reward_badge and self.reward_badge not in user.badges:
                user.badges.append(self.reward_badge)
            user.save()
            
            self.save()
    
    def to_dict(self):
        """Convert challenge to dictionary"""
        return {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'rules': self.rules,
            'reward_xp': self.reward_xp,
            'reward_badge': self.reward_badge.to_dict() if self.reward_badge else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'participants_count': len(self.participants) if self.participants else 0,
            'completers_count': len(self.completers) if self.completers else 0,
            'is_active': self.is_active,
            'is_ongoing': self.is_ongoing(),
        }
    
    def __str__(self):
        return f"Challenge: {self.title}"


# XP reward constants
XP_REWARDS = {
    'submit_recipe': 50,
    'cook': 10,
    'comment': 5,
    'share': 5,
    'rate': 5,
    'follow': 2,
    'upload_photo': 15,
}


def award_xp_for_action(user, action_type, target_id=None, metadata=None):
    """
    Award XP to user for an action and create UserAction record
    
    Args:
        user: User document
        action_type: Type of action (must be in XP_REWARDS)
        target_id: Optional ID of target object
        metadata: Optional additional data
    
    Returns:
        UserAction document
    """
    xp_amount = XP_REWARDS.get(action_type, 0)
    
    # Create user action record
    user_action = UserAction(
        user=user,
        action_type=action_type,
        target_id=target_id,
        xp_awarded=xp_amount,
        metadata=metadata or {}
    )
    user_action.save()
    
    # Add XP to user
    user.add_xp(xp_amount)
    user.save()
    
    # Check for badge eligibility
    check_badge_eligibility(user, action_type)
    
    return user_action


def check_badge_eligibility(user, action_type):
    """Check if user earned any badges based on their actions"""
    # Example badge checks
    
    # "First Recipe" badge
    if action_type == 'submit_recipe':
        recipe_count = UserAction.objects(
            user=user,
            action_type='submit_recipe'
        ).count()
        
        if recipe_count == 1:
            first_recipe_badge = Badge.objects(name="First Recipe").first()
            if first_recipe_badge and first_recipe_badge not in user.badges:
                user.badges.append(first_recipe_badge)
                user.save()
    
    # "Master Chef" badge - 50 recipes
    if action_type == 'submit_recipe':
        recipe_count = UserAction.objects(
            user=user,
            action_type='submit_recipe'
        ).count()
        
        if recipe_count >= 50:
            master_badge = Badge.objects(name="Master Chef").first()
            if master_badge and master_badge not in user.badges:
                user.badges.append(master_badge)
                user.save()
    
    # "Social Butterfly" badge - 100 comments
    if action_type == 'comment':
        comment_count = UserAction.objects(
            user=user,
            action_type='comment'
        ).count()
        
        if comment_count >= 100:
            social_badge = Badge.objects(name="Social Butterfly").first()
            if social_badge and social_badge not in user.badges:
                user.badges.append(social_badge)
                user.save()
