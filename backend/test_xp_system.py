"""
Test script for XP and Level System
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.gamification.xp_system import (
    calculate_level_from_xp,
    get_xp_for_next_level,
    get_xp_reward,
    check_level_up,
    get_level_name,
    LEVEL_THRESHOLDS,
    XP_REWARDS
)

def test_xp_system():
    """Test XP calculation functions"""
    print("=" * 60)
    print("XP & LEVEL SYSTEM TEST")
    print("=" * 60)
    
    # Test 1: Level Thresholds
    print("\n1. LEVEL THRESHOLDS:")
    print("-" * 60)
    for level in range(1, 11):
        xp_required = LEVEL_THRESHOLDS.get(level, 0)
        level_name = get_level_name(level)
        print(f"Level {level:2d} ({level_name:20s}): {xp_required:5d} XP")
    
    # Test 2: XP Rewards
    print("\n2. XP REWARDS FOR ACTIONS:")
    print("-" * 60)
    for action, xp in XP_REWARDS.items():
        print(f"{action:20s}: +{xp} XP")
    
    # Test 3: Calculate Level from XP
    print("\n3. LEVEL CALCULATION FROM XP:")
    print("-" * 60)
    test_xp_values = [0, 50, 100, 200, 300, 500, 1000, 2000, 5000]
    for xp in test_xp_values:
        level = calculate_level_from_xp(xp)
        level_name = get_level_name(level)
        print(f"XP: {xp:5d} → Level {level:2d} ({level_name})")
    
    # Test 4: XP Progress to Next Level
    print("\n4. XP PROGRESS CALCULATION:")
    print("-" * 60)
    test_user_xp = 150
    progress = get_xp_for_next_level(test_user_xp)
    print(f"User XP: {test_user_xp}")
    print(f"Current Level: {progress['current_level']}")
    print(f"Next Level: {progress['next_level']}")
    print(f"XP Progress: {progress['xp_progress']}/{progress['next_level_xp'] - progress['current_level_xp']}")
    print(f"XP Needed: {progress['xp_needed']}")
    print(f"Progress: {progress['progress_percentage']}%")
    
    # Test 5: Level Up Detection
    print("\n5. LEVEL UP DETECTION:")
    print("-" * 60)
    test_scenarios = [
        (90, 110),   # Level up from 1 to 2
        (240, 260),  # Level up from 2 to 3
        (100, 300),  # Level up from 2 to 3 (big jump)
    ]
    for old_xp, new_xp in test_scenarios:
        result = check_level_up(old_xp, new_xp)
        if result:
            print(f"XP: {old_xp} → {new_xp}: LEVEL UP! {result['old_level']} → {result['new_level']}")
        else:
            print(f"XP: {old_xp} → {new_xp}: No level up")
    
    # Test 6: XP Rewards with Bonuses
    print("\n6. XP REWARDS WITH BONUSES:")
    print("-" * 60)
    
    # Base recipe cooked
    base_xp = get_xp_reward('recipe_cooked')
    print(f"Recipe Cooked (base): +{base_xp} XP")
    
    # Recipe cooked with photo
    photo_xp = get_xp_reward('recipe_cooked', has_photo=True)
    print(f"Recipe Cooked + Photo: +{photo_xp} XP")
    
    # Recipe cooked with rating
    rating_xp = get_xp_reward('recipe_cooked', has_rating=True)
    print(f"Recipe Cooked + Rating: +{rating_xp} XP")
    
    # Recipe cooked with both
    full_xp = get_xp_reward('recipe_cooked', has_photo=True, has_rating=True)
    print(f"Recipe Cooked + Photo + Rating: +{full_xp} XP")
    
    print("\n" + "=" * 60)
    print("✅ XP SYSTEM TEST COMPLETED SUCCESSFULLY!")
    print("=" * 60)


def test_user_xp_methods():
    """Test User model XP methods"""
    from apps.users.models import User
    
    print("\n" + "=" * 60)
    print("USER MODEL XP METHODS TEST")
    print("=" * 60)
    
    # Find test user
    try:
        user = User.objects.get(username='testchef')
        print(f"\n✅ Found user: {user.username}")
        print(f"Current XP: {user.xp}")
        print(f"Current Level: {user.level}")
        print(f"Level Title: {user.get_level_title()}")
        
        # Test XP progress
        print("\nXP Progress:")
        progress = user.get_xp_progress()
        for key, value in progress.items():
            print(f"  {key}: {value}")
        
        # Test adding XP (without saving)
        print("\n--- Simulating XP Gain (not saved) ---")
        old_xp = user.xp
        result = user.add_xp(50, action_type='recipe_created')
        
        print(f"XP Gained: +{result['xp_gained']}")
        print(f"New XP: {result['new_xp']}")
        print(f"New Level: {result['new_level']}")
        if result['level_up']:
            print(f"🎉 LEVEL UP! {result['level_up']['old_level']} → {result['level_up']['new_level']}")
        else:
            print("No level up")
        
        # Reset XP for next test
        user.xp = old_xp
        user.level = calculate_level_from_xp(old_xp)
        
        print("\n✅ User XP methods test completed!")
        
    except User.DoesNotExist:
        print("\n⚠️  Test user 'testchef' not found. Skipping user model test.")
    
    print("=" * 60)


if __name__ == '__main__':
    test_xp_system()
    test_user_xp_methods()
