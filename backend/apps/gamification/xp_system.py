"""
XP and Level System for Gamification
Handles XP calculation, level progression, and rewards
"""

# Level thresholds - XP required for each level
LEVEL_THRESHOLDS = {
    1: 0,
    2: 100,
    3: 250,
    4: 500,
    5: 850,
    6: 1300,
    7: 1900,
    8: 2600,
    9: 3400,
    10: 4300,
    11: 5300,
    12: 6500,
    13: 7900,
    14: 9500,
    15: 11300,
    16: 13300,
    17: 15500,
    18: 18000,
    19: 20800,
    20: 24000,
}

# XP rewards for different actions
XP_REWARDS = {
    'recipe_created': 50,
    'recipe_cooked': 10,
    'photo_uploaded': 5,
    'recipe_rated': 3,
    'comment_posted': 2,
    'recipe_liked': 1,
    'user_followed': 5,
    'daily_login': 5,
    'first_recipe': 100,  # Bonus for first recipe
    'recipe_featured': 200,  # Admin featured recipe
}


def calculate_level_from_xp(xp):
    """
    Calculate user level based on total XP
    
    Args:
        xp (int): Total XP points
        
    Returns:
        int: Current level (1-20)
    """
    level = 1
    for lvl, threshold in sorted(LEVEL_THRESHOLDS.items(), reverse=True):
        if xp >= threshold:
            level = lvl
            break
    return level


def get_xp_for_next_level(current_xp):
    """
    Get XP required for the next level
    
    Args:
        current_xp (int): Current total XP
        
    Returns:
        dict: {
            'current_level': int,
            'next_level': int,
            'current_level_xp': int,
            'next_level_xp': int,
            'xp_progress': int,
            'xp_needed': int,
            'progress_percentage': float
        }
    """
    current_level = calculate_level_from_xp(current_xp)
    next_level = min(current_level + 1, max(LEVEL_THRESHOLDS.keys()))
    
    current_level_xp = LEVEL_THRESHOLDS[current_level]
    next_level_xp = LEVEL_THRESHOLDS.get(next_level, current_level_xp)
    
    xp_progress = current_xp - current_level_xp
    xp_needed = next_level_xp - current_xp
    
    if next_level_xp > current_level_xp:
        progress_percentage = (xp_progress / (next_level_xp - current_level_xp)) * 100
    else:
        progress_percentage = 100  # Max level reached
    
    return {
        'current_level': current_level,
        'next_level': next_level,
        'current_level_xp': current_level_xp,
        'next_level_xp': next_level_xp,
        'xp_progress': xp_progress,
        'xp_needed': max(0, xp_needed),
        'progress_percentage': round(progress_percentage, 2)
    }


def get_xp_reward(action_type, **kwargs):
    """
    Get XP reward for a specific action
    
    Args:
        action_type (str): Type of action (e.g., 'recipe_created', 'recipe_cooked')
        **kwargs: Additional parameters (e.g., has_photo=True, has_rating=True)
        
    Returns:
        int: XP points to award
    """
    base_xp = XP_REWARDS.get(action_type, 0)
    
    # Bonus XP for additional content
    if action_type == 'recipe_cooked':
        if kwargs.get('has_photo'):
            base_xp += XP_REWARDS['photo_uploaded']
        if kwargs.get('has_rating'):
            base_xp += XP_REWARDS['recipe_rated']
    
    return base_xp


def check_level_up(old_xp, new_xp):
    """
    Check if user leveled up after gaining XP
    
    Args:
        old_xp (int): XP before action
        new_xp (int): XP after action
        
    Returns:
        dict or None: {
            'leveled_up': bool,
            'old_level': int,
            'new_level': int,
            'levels_gained': int
        } or None if no level up
    """
    old_level = calculate_level_from_xp(old_xp)
    new_level = calculate_level_from_xp(new_xp)
    
    if new_level > old_level:
        return {
            'leveled_up': True,
            'old_level': old_level,
            'new_level': new_level,
            'levels_gained': new_level - old_level
        }
    
    return None


def get_level_name(level):
    """
    Get a descriptive name for a level
    
    Args:
        level (int): User level
        
    Returns:
        str: Level name/title
    """
    level_names = {
        1: "Novice Cook",
        2: "Home Cook",
        3: "Kitchen Helper",
        4: "Prep Cook",
        5: "Line Cook",
        6: "Station Chef",
        7: "Sous Chef",
        8: "Head Chef",
        9: "Executive Chef",
        10: "Master Chef",
        11: "Culinary Expert",
        12: "Kitchen Maestro",
        13: "Gastronomy Guru",
        14: "Culinary Artist",
        15: "Food Innovator",
        16: "Michelin Star",
        17: "Culinary Legend",
        18: "Master Cuisiner",
        19: "Global Icon",
        20: "Culinary God",
    }
    return level_names.get(level, f"Level {level}")


def calculate_total_xp_for_level(level):
    """
    Calculate total XP required to reach a specific level
    
    Args:
        level (int): Target level
        
    Returns:
        int: Total XP required
    """
    return LEVEL_THRESHOLDS.get(level, 0)
