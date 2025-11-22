"""
Helper functions to create notifications for various events
"""
from .notification_model import Notification


def notify_new_comment(recipe_author, commenter, recipe, comment):
    """Notify recipe author when someone comments on their recipe"""
    if str(recipe_author.id) == str(commenter.id):
        return  # Don't notify yourself
    
    Notification.create_notification(
        recipient=recipe_author,
        sender=commenter,
        notification_type='recipe_comment',
        title='New comment on your recipe',
        message=f'{commenter.username} commented on "{recipe.title}"',
        related_object_type='recipe',
        related_object_id=str(recipe.id),
        metadata={
            'recipe_slug': recipe.slug,
            'recipe_title': recipe.title,
            'comment_id': str(comment.id),
        }
    )


def notify_comment_like(comment_author, liker, comment):
    """Notify comment author when someone likes their comment"""
    if str(comment_author.id) == str(liker.id):
        return  # Don't notify yourself
    
    Notification.create_notification(
        recipient=comment_author,
        sender=liker,
        notification_type='comment_like',
        title='Someone liked your comment',
        message=f'{liker.username} liked your comment',
        related_object_type='comment',
        related_object_id=str(comment.id),
        metadata={'comment_id': str(comment.id)}
    )


def notify_badge_earned(user, badge):
    """Notify user when they earn a new badge"""
    Notification.create_notification(
        recipient=user,
        notification_type='badge_earned',
        title='New badge earned!',
        message=f'Congratulations! You earned the "{badge.name}" badge',
        related_object_type='badge',
        related_object_id=str(badge.id),
        metadata={
            'badge_name': badge.name,
            'badge_icon': badge.icon,
            'badge_rarity': badge.rarity,
        }
    )


def notify_level_up(user, new_level):
    """Notify user when they level up"""
    Notification.create_notification(
        recipient=user,
        notification_type='level_up',
        title='Level Up!',
        message=f'Congratulations! You reached Level {new_level}',
        related_object_type='user',
        related_object_id=str(user.id),
        metadata={'new_level': new_level}
    )


def notify_recipe_cooked(recipe_author, cooker, recipe):
    """Notify recipe author when someone cooks their recipe"""
    if str(recipe_author.id) == str(cooker.id):
        return  # Don't notify yourself
    
    Notification.create_notification(
        recipient=recipe_author,
        sender=cooker,
        notification_type='recipe_cooked',
        title='Someone cooked your recipe!',
        message=f'{cooker.username} cooked "{recipe.title}"',
        related_object_type='recipe',
        related_object_id=str(recipe.id),
        metadata={
            'recipe_slug': recipe.slug,
            'recipe_title': recipe.title,
        }
    )


def notify_new_follower(followed_user, follower):
    """Notify user when someone follows them"""
    Notification.create_notification(
        recipient=followed_user,
        sender=follower,
        notification_type='new_follower',
        title='New follower',
        message=f'{follower.username} started following you',
        related_object_type='user',
        related_object_id=str(follower.id),
        metadata={'follower_username': follower.username}
    )
