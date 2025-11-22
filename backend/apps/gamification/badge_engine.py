"""
Badge Engine - Automatic badge awarding system
Checks user progress and awards badges when criteria are met
"""
from .models import Badge, UserAction, CookedRecipe
from apps.recipes.models import Recipe


def check_and_award_badges(user):
    """
    Check all badge criteria and award any newly earned badges
    
    Args:
        user: User object
        
    Returns:
        list: List of newly awarded badge dicts
    """
    newly_awarded = []
    all_badges = Badge.objects(is_active=True)
    
    for badge in all_badges:
        # Skip if user already has this badge
        if str(badge.id) in user.badges:
            continue
        
        # Check if user meets criteria
        if meets_criteria(user, badge):
            # Award badge
            user.badges.append(str(badge.id))
            
            # Award bonus XP if badge has it
            if badge.xp_reward > 0:
                user.add_xp(badge.xp_reward, action_type='badge_earned')
            
            # Send notification
            try:
                from .notification_helpers import notify_badge_earned
                notify_badge_earned(user, badge)
            except Exception as e:
                pass  # Don't fail if notification fails
            
            newly_awarded.append(badge.to_dict())
    
    # Save user if badges were awarded
    if newly_awarded:
        user.save()
    
    return newly_awarded


def meets_criteria(user, badge):
    """
    Check if user meets the criteria for a badge
    
    Args:
        user: User object
        badge: Badge object
        
    Returns:
        bool: True if criteria met
    """
    criteria_type = badge.criteria_type
    criteria_value = badge.criteria_value
    
    if criteria_type == 'recipes_created':
        count = Recipe.objects(author=user).count()
        return count >= criteria_value
    
    elif criteria_type == 'recipes_cooked':
        count = CookedRecipe.objects(user=user).count()
        return count >= criteria_value
    
    elif criteria_type == 'total_xp':
        return user.xp >= criteria_value
    
    elif criteria_type == 'level_reached':
        return user.level >= criteria_value
    
    elif criteria_type == 'followers':
        return len(user.followers) >= criteria_value
    
    elif criteria_type == 'likes_received':
        # Count total likes on user's recipes
        user_recipes = Recipe.objects(author=user)
        total_likes = sum(getattr(recipe, 'likes_count', 0) for recipe in user_recipes)
        return total_likes >= criteria_value
    
    elif criteria_type == 'comments_posted':
        count = UserAction.objects(user=user, action_type='comment_posted').count()
        return count >= criteria_value
    
    elif criteria_type == 'special':
        # Special badges are manually awarded by admin
        return False
    
    return False


def get_user_badges(user):
    """
    Get all badges earned by a user
    
    Args:
        user: User object
        
    Returns:
        list: List of badge dicts
    """
    if not user.badges:
        return []
    
    badges = Badge.objects(id__in=user.badges)
    return [badge.to_dict() for badge in badges]


def get_badge_progress(user, badge):
    """
    Get user's progress towards a specific badge
    
    Args:
        user: User object
        badge: Badge object
        
    Returns:
        dict: Progress information
    """
    criteria_type = badge.criteria_type
    criteria_value = badge.criteria_value
    current_value = 0
    
    if criteria_type == 'recipes_created':
        current_value = Recipe.objects(author=user).count()
    elif criteria_type == 'recipes_cooked':
        current_value = CookedRecipe.objects(user=user).count()
    elif criteria_type == 'total_xp':
        current_value = user.xp
    elif criteria_type == 'level_reached':
        current_value = user.level
    elif criteria_type == 'followers':
        current_value = len(user.followers)
    elif criteria_type == 'likes_received':
        user_recipes = Recipe.objects(author=user)
        current_value = sum(getattr(recipe, 'likes_count', 0) for recipe in user_recipes)
    elif criteria_type == 'comments_posted':
        current_value = UserAction.objects(user=user, action_type='comment_posted').count()
    
    percentage = min(100, (current_value / criteria_value * 100)) if criteria_value > 0 else 0
    
    return {
        'badge': badge.to_dict(),
        'current_value': current_value,
        'required_value': criteria_value,
        'percentage': round(percentage, 2),
        'earned': str(badge.id) in user.badges
    }


def get_all_badges_progress(user):
    """
    Get progress for all badges
    
    Args:
        user: User object
        
    Returns:
        dict: {
            'earned': list of earned badges,
            'in_progress': list of badges being worked on,
            'locked': list of locked badges
        }
    """
    all_badges = Badge.objects(is_active=True)
    
    earned = []
    in_progress = []
    locked = []
    
    for badge in all_badges:
        progress = get_badge_progress(user, badge)
        
        if progress['earned']:
            earned.append(progress)
        elif progress['percentage'] > 0:
            in_progress.append(progress)
        else:
            locked.append(progress)
    
    return {
        'earned': earned,
        'in_progress': in_progress,
        'locked': locked
    }


def create_default_badges():
    """
    Create default badge set if none exist
    
    Returns:
        int: Number of badges created
    """
    existing_count = Badge.objects.count()
    if existing_count > 0:
        print(f"Badges already exist ({existing_count}). Skipping creation.")
        return 0
    
    default_badges = [
        # Recipe Creation Badges
        {
            'name': 'First Recipe',
            'description': 'Create your first recipe',
            'icon': '📝',
            'criteria_type': 'recipes_created',
            'criteria_value': 1,
            'rarity': 'common',
            'xp_reward': 10
        },
        {
            'name': 'Recipe Author',
            'description': 'Create 5 recipes',
            'icon': '✍️',
            'criteria_type': 'recipes_created',
            'criteria_value': 5,
            'rarity': 'common',
            'xp_reward': 25
        },
        {
            'name': 'Prolific Creator',
            'description': 'Create 10 recipes',
            'icon': '📚',
            'criteria_type': 'recipes_created',
            'criteria_value': 10,
            'rarity': 'rare',
            'xp_reward': 50
        },
        {
            'name': 'Recipe Master',
            'description': 'Create 25 recipes',
            'icon': '⭐',
            'criteria_type': 'recipes_created',
            'criteria_value': 25,
            'rarity': 'epic',
            'xp_reward': 100
        },
        
        # Cooking Badges
        {
            'name': 'First Cook',
            'description': 'Cook your first recipe',
            'icon': '🍳',
            'criteria_type': 'recipes_cooked',
            'criteria_value': 1,
            'rarity': 'common',
            'xp_reward': 10
        },
        {
            'name': 'Chef Apprentice',
            'description': 'Cook 10 recipes',
            'icon': '👨‍🍳',
            'criteria_type': 'recipes_cooked',
            'criteria_value': 10,
            'rarity': 'rare',
            'xp_reward': 50
        },
        {
            'name': 'Master Chef',
            'description': 'Cook 50 recipes',
            'icon': '🏆',
            'criteria_type': 'recipes_cooked',
            'criteria_value': 50,
            'rarity': 'epic',
            'xp_reward': 150
        },
        {
            'name': 'Culinary Legend',
            'description': 'Cook 100 recipes',
            'icon': '👑',
            'criteria_type': 'recipes_cooked',
            'criteria_value': 100,
            'rarity': 'legendary',
            'xp_reward': 300
        },
        
        # XP Badges
        {
            'name': 'Rising Star',
            'description': 'Reach 500 XP',
            'icon': '✨',
            'criteria_type': 'total_xp',
            'criteria_value': 500,
            'rarity': 'rare',
            'xp_reward': 25
        },
        {
            'name': 'XP Champion',
            'description': 'Reach 2000 XP',
            'icon': '💫',
            'criteria_type': 'total_xp',
            'criteria_value': 2000,
            'rarity': 'epic',
            'xp_reward': 100
        },
        
        # Level Badges
        {
            'name': 'Level 5 Achieved',
            'description': 'Reach Level 5',
            'icon': '🎖️',
            'criteria_type': 'level_reached',
            'criteria_value': 5,
            'rarity': 'rare',
            'xp_reward': 50
        },
        {
            'name': 'Level 10 Achieved',
            'description': 'Reach Level 10',
            'icon': '🏅',
            'criteria_type': 'level_reached',
            'criteria_value': 10,
            'rarity': 'epic',
            'xp_reward': 100
        },
        
        # Social Badges
        {
            'name': 'Social Butterfly',
            'description': 'Get 50 followers',
            'icon': '🦋',
            'criteria_type': 'followers',
            'criteria_value': 50,
            'rarity': 'epic',
            'xp_reward': 75
        },
        {
            'name': 'Community Favorite',
            'description': 'Receive 100 likes on your recipes',
            'icon': '❤️',
            'criteria_type': 'likes_received',
            'criteria_value': 100,
            'rarity': 'epic',
            'xp_reward': 100
        },
        {
            'name': 'Conversationalist',
            'description': 'Post 50 comments',
            'icon': '💬',
            'criteria_type': 'comments_posted',
            'criteria_value': 50,
            'rarity': 'rare',
            'xp_reward': 50
        },
        
        # Special Badges
        {
            'name': 'Early Adopter',
            'description': 'Join during the first month',
            'icon': '🎉',
            'criteria_type': 'special',
            'criteria_value': 1,
            'rarity': 'legendary',
            'xp_reward': 200
        },
        {
            'name': 'Beta Tester',
            'description': 'Help test the platform',
            'icon': '🧪',
            'criteria_type': 'special',
            'criteria_value': 1,
            'rarity': 'legendary',
            'xp_reward': 150
        },
    ]
    
    created_count = 0
    for badge_data in default_badges:
        badge = Badge(**badge_data)
        badge.save()
        created_count += 1
    
    return created_count
