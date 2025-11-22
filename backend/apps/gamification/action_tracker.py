"""
User Action Tracking System
Automatically track user actions and award XP
"""
import json
from datetime import datetime
from .models import UserAction
from .xp_system import get_xp_reward


def track_action(user, action_type, target_recipe=None, **kwargs):
    """
    Track a user action and award XP
    
    Args:
        user: User object
        action_type (str): Type of action (recipe_created, recipe_cooked, etc.)
        target_recipe: Recipe object (optional)
        **kwargs: Additional data for metadata (has_photo, has_rating, etc.)
        
    Returns:
        dict: {
            'action': UserAction object,
            'xp_result': dict from user.add_xp(),
            'success': bool
        }
    """
    try:
        # Calculate XP reward
        xp_amount = get_xp_reward(action_type, **kwargs)
        
        # Award XP to user
        xp_result = user.add_xp(xp_amount, action_type=action_type)
        
        # Save user with new XP
        user.save()
        
        # Create action record
        metadata = json.dumps(kwargs) if kwargs else None
        action = UserAction(
            user=user,
            action_type=action_type,
            target_recipe=target_recipe,
            xp_awarded=xp_amount,
            metadata=metadata,
            created_at=datetime.utcnow()
        )
        action.save()
        
        return {
            'action': action,
            'xp_result': xp_result,
            'success': True,
            'message': f'Earned {xp_amount} XP for {action_type}'
        }
        
    except Exception as e:
        return {
            'action': None,
            'xp_result': None,
            'success': False,
            'message': f'Error tracking action: {str(e)}'
        }


def get_user_actions(user, action_type=None, limit=50):
    """
    Get user's recent actions
    
    Args:
        user: User object
        action_type (str, optional): Filter by action type
        limit (int): Maximum number of actions to return
        
    Returns:
        list: List of UserAction objects
    """
    query = UserAction.objects(user=user).order_by('-created_at')
    
    if action_type:
        query = query.filter(action_type=action_type)
    
    return list(query.limit(limit))


def get_action_stats(user):
    """
    Get user's action statistics
    
    Args:
        user: User object
        
    Returns:
        dict: Statistics by action type
    """
    actions = UserAction.objects(user=user)
    
    stats = {
        'total_actions': actions.count(),
        'total_xp_earned': sum(action.xp_awarded for action in actions),
        'by_type': {}
    }
    
    # Count actions by type
    for action_type in ['recipe_created', 'recipe_cooked', 'photo_uploaded', 
                       'recipe_rated', 'comment_posted', 'recipe_liked', 
                       'user_followed', 'daily_login', 'badge_earned']:
        type_actions = actions.filter(action_type=action_type)
        count = type_actions.count()
        xp = sum(action.xp_awarded for action in type_actions)
        
        stats['by_type'][action_type] = {
            'count': count,
            'xp_earned': xp
        }
    
    return stats


def get_recent_activity(user, days=7, limit=20):
    """
    Get user's recent activity
    
    Args:
        user: User object
        days (int): Number of days to look back
        limit (int): Maximum number of actions
        
    Returns:
        list: Recent actions with formatted data
    """
    from datetime import timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    actions = UserAction.objects(
        user=user,
        created_at__gte=cutoff_date
    ).order_by('-created_at').limit(limit)
    
    activity = []
    for action in actions:
        activity.append({
            'id': str(action.id),
            'action_type': action.action_type,
            'xp_awarded': action.xp_awarded,
            'recipe_id': str(action.target_recipe.id) if action.target_recipe else None,
            'recipe_title': action.target_recipe.title if action.target_recipe else None,
            'created_at': action.created_at.isoformat() if action.created_at else None,
            'metadata': json.loads(action.metadata) if action.metadata else {}
        })
    
    return activity


def track_recipe_creation(user, recipe):
    """
    Track recipe creation action
    
    Args:
        user: User object
        recipe: Recipe object
        
    Returns:
        dict: Action tracking result
    """
    # Check if this is user's first recipe for bonus XP
    from .models import UserAction
    previous_recipes = UserAction.objects(
        user=user,
        action_type='recipe_created'
    ).count()
    
    is_first = previous_recipes == 0
    action_type = 'first_recipe' if is_first else 'recipe_created'
    
    return track_action(user, action_type, target_recipe=recipe, is_first=is_first)


def track_recipe_cooked(user, recipe, has_photo=False, has_rating=False):
    """
    Track recipe cooked action with optional bonuses
    
    Args:
        user: User object
        recipe: Recipe object
        has_photo (bool): Whether user uploaded a photo
        has_rating (bool): Whether user provided a rating
        
    Returns:
        dict: Action tracking result
    """
    return track_action(
        user,
        'recipe_cooked',
        target_recipe=recipe,
        has_photo=has_photo,
        has_rating=has_rating
    )


def track_comment_posted(user, recipe):
    """Track comment posted action"""
    return track_action(user, 'comment_posted', target_recipe=recipe)


def track_recipe_liked(user, recipe):
    """Track recipe liked action"""
    return track_action(user, 'recipe_liked', target_recipe=recipe)


def track_user_followed(user, followed_user):
    """Track user followed action"""
    return track_action(user, 'user_followed', followed_user_id=str(followed_user.id))


def track_daily_login(user):
    """
    Track daily login (award XP once per day)
    
    Args:
        user: User object
        
    Returns:
        dict: Action tracking result or None if already logged in today
    """
    from datetime import date
    
    # Check if user already logged in today
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    
    existing_login = UserAction.objects(
        user=user,
        action_type='daily_login',
        created_at__gte=today_start
    ).first()
    
    if existing_login:
        return {
            'success': False,
            'message': 'Already logged in today',
            'action': None,
            'xp_result': None
        }
    
    return track_action(user, 'daily_login')
