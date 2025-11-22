"""
Notification model for user notifications
"""
from mongoengine import (
    Document, StringField, ReferenceField, BooleanField, 
    DateTimeField, DictField
)
from datetime import datetime


class Notification(Document):
    """Notification document for user alerts"""
    
    recipient = ReferenceField('User', required=True)
    sender = ReferenceField('User', required=False)  # Optional, can be system notification
    
    notification_type = StringField(required=True, choices=[
        'new_follower',      # Someone followed you
        'recipe_comment',    # Someone commented on your recipe
        'comment_like',      # Someone liked your comment
        'recipe_like',       # Someone liked your recipe
        'badge_earned',      # You earned a new badge
        'level_up',          # You leveled up
        'recipe_cooked',     # Someone cooked your recipe
        'comment_reply',     # Someone replied to your comment
    ])
    
    title = StringField(required=True, max_length=200)
    message = StringField(required=True, max_length=500)
    
    # Related object references (stored as strings for flexibility)
    related_object_type = StringField(choices=['recipe', 'comment', 'user', 'badge', 'none'])
    related_object_id = StringField()
    
    # Additional data (e.g., recipe slug, badge name, etc.)
    metadata = DictField()
    
    is_read = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    read_at = DateTimeField()
    
    meta = {
        'collection': 'notifications',
        'indexes': [
            'recipient',
            '-created_at',
            'is_read',
            ('recipient', '-created_at'),
            ('recipient', 'is_read'),
        ],
        'ordering': ['-created_at']
    }
    
    def to_dict(self):
        """Convert notification to dictionary"""
        return {
            'id': str(self.id),
            'recipient': str(self.recipient.id) if self.recipient else None,
            'sender': {
                'id': str(self.sender.id),
                'username': self.sender.username,
                'level': self.sender.level,
            } if self.sender else None,
            'type': self.notification_type,
            'title': self.title,
            'message': self.message,
            'related_object': {
                'type': self.related_object_type,
                'id': self.related_object_id,
            } if self.related_object_type and self.related_object_id else None,
            'metadata': self.metadata or {},
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None,
        }
    
    @classmethod
    def create_notification(cls, recipient, notification_type, title, message, 
                          sender=None, related_object_type=None, 
                          related_object_id=None, metadata=None):
        """Helper method to create a notification"""
        notification = cls(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            title=title,
            message=message,
            related_object_type=related_object_type or 'none',
            related_object_id=related_object_id,
            metadata=metadata or {}
        )
        notification.save()
        return notification
