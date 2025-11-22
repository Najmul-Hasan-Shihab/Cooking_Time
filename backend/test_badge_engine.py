"""
Test script for Badge Engine
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.gamification.badge_engine import (
    create_default_badges,
    check_and_award_badges,
    get_user_badges,
    get_all_badges_progress,
    meets_criteria
)
from apps.gamification.models import Badge


def test_badge_system():
    """Test badge engine functionality"""
    print("=" * 60)
    print("BADGE ENGINE TEST")
    print("=" * 60)
    
    # Test 1: Create Default Badges
    print("\n" + "-" * 60)
    print("TEST 1: Create Default Badges")
    print("-" * 60)
    
    count = create_default_badges()
    if count > 0:
        print(f"✅ Created {count} default badges")
    else:
        print(f"✅ Badges already exist")
    
    # Show all badges
    all_badges = Badge.objects(is_active=True)
    print(f"\nTotal badges in system: {all_badges.count()}")
    print("\nBadge List:")
    for badge in all_badges:
        print(f"  {badge.icon} {badge.name} ({badge.rarity})")
        print(f"     {badge.description}")
        print(f"     Criteria: {badge.criteria_type} >= {badge.criteria_value}")
        print(f"     Reward: +{badge.xp_reward} XP")
    
    # Test 2: Check User Badges
    print("\n" + "-" * 60)
    print("TEST 2: Check User Badges")
    print("-" * 60)
    
    try:
        user = User.objects.get(username='testchef')
        print(f"✅ Found user: {user.username}")
        print(f"Current XP: {user.xp}")
        print(f"Current Level: {user.level} ({user.get_level_title()})")
        print(f"Current Badges: {len(user.badges)}")
        
        # Check for new badges
        print("\nChecking for new badges...")
        newly_awarded = check_and_award_badges(user)
        
        if newly_awarded:
            print(f"\n🎉 Earned {len(newly_awarded)} new badge(s)!")
            for badge in newly_awarded:
                print(f"  {badge['icon']} {badge['name']}")
                print(f"     {badge['description']}")
                print(f"     +{badge['xp_reward']} XP bonus!")
        else:
            print("No new badges earned at this time.")
        
        # Test 3: Get User's Badges
        print("\n" + "-" * 60)
        print("TEST 3: Get User's Earned Badges")
        print("-" * 60)
        
        earned_badges = get_user_badges(user)
        print(f"Total earned badges: {len(earned_badges)}")
        if earned_badges:
            for badge in earned_badges:
                print(f"  {badge['icon']} {badge['name']} ({badge['rarity']})")
        
        # Test 4: Badge Progress
        print("\n" + "-" * 60)
        print("TEST 4: Badge Progress Tracking")
        print("-" * 60)
        
        progress = get_all_badges_progress(user)
        
        print(f"\n📊 Progress Summary:")
        print(f"  Earned: {len(progress['earned'])}")
        print(f"  In Progress: {len(progress['in_progress'])}")
        print(f"  Locked: {len(progress['locked'])}")
        
        if progress['in_progress']:
            print(f"\n🎯 Badges In Progress:")
            for p in progress['in_progress'][:5]:  # Show first 5
                badge = p['badge']
                print(f"  {badge['icon']} {badge['name']}")
                print(f"     Progress: {p['current_value']}/{p['required_value']} ({p['percentage']:.1f}%)")
        
        # Test 5: Check Specific Criteria
        print("\n" + "-" * 60)
        print("TEST 5: Check Specific Badge Criteria")
        print("-" * 60)
        
        first_recipe_badge = Badge.objects(name='First Recipe').first()
        if first_recipe_badge:
            meets = meets_criteria(user, first_recipe_badge)
            print(f"First Recipe badge: {'✅ Earned' if meets else '❌ Not earned'}")
        
        chef_apprentice = Badge.objects(name='Chef Apprentice').first()
        if chef_apprentice:
            meets = meets_criteria(user, chef_apprentice)
            print(f"Chef Apprentice badge: {'✅ Earned' if meets else '❌ Not earned'}")
        
        # Test 6: Final Stats
        print("\n" + "-" * 60)
        print("TEST 6: Final User Stats")
        print("-" * 60)
        
        user.reload()  # Refresh from database
        print(f"Final XP: {user.xp}")
        print(f"Final Level: {user.level} ({user.get_level_title()})")
        print(f"Total Badges: {len(user.badges)}")
        
        xp_progress = user.get_xp_progress()
        print(f"XP Progress: {xp_progress['xp_progress']}/{xp_progress['next_level_xp'] - xp_progress['current_level_xp']} ({xp_progress['progress_percentage']:.2f}%)")
        
        print("\n" + "=" * 60)
        print("✅ BADGE ENGINE TEST COMPLETED!")
        print("=" * 60)
        
    except User.DoesNotExist:
        print("\n❌ Test user 'testchef' not found")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_badge_system()
