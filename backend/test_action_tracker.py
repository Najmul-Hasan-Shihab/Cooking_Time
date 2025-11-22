"""
Test script for User Action Tracking System
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.recipes.models import Recipe
from apps.gamification.action_tracker import (
    track_action,
    track_recipe_creation,
    track_recipe_cooked,
    get_user_actions,
    get_action_stats,
    get_recent_activity
)


def test_action_tracking():
    """Test action tracking functionality"""
    print("=" * 60)
    print("USER ACTION TRACKING SYSTEM TEST")
    print("=" * 60)
    
    # Get test user
    try:
        user = User.objects.get(username='testchef')
        print(f"\n✅ Found user: {user.username}")
        print(f"Initial XP: {user.xp}")
        print(f"Initial Level: {user.level} ({user.get_level_title()})")
        
        # Get a recipe for testing
        recipe = Recipe.objects.first()
        if not recipe:
            print("\n⚠️  No recipes found. Skipping recipe-related tests.")
            return
        
        print(f"\n📖 Test Recipe: {recipe.title}")
        
        # Test 1: Track Recipe Cooked (base)
        print("\n" + "-" * 60)
        print("TEST 1: Track Recipe Cooked (base)")
        print("-" * 60)
        
        old_xp = user.xp
        result = track_recipe_cooked(user, recipe, has_photo=False, has_rating=False)
        
        if result['success']:
            print(f"✅ Action tracked successfully!")
            print(f"   XP Gained: +{result['xp_result']['xp_gained']}")
            print(f"   New XP: {result['xp_result']['new_xp']}")
            print(f"   New Level: {result['xp_result']['new_level']}")
            if result['xp_result']['level_up']:
                print(f"   🎉 LEVEL UP! {result['xp_result']['level_up']['old_level']} → {result['xp_result']['level_up']['new_level']}")
        else:
            print(f"❌ Failed: {result['message']}")
        
        # Test 2: Track Recipe Cooked (with photo and rating)
        print("\n" + "-" * 60)
        print("TEST 2: Track Recipe Cooked (with photo + rating)")
        print("-" * 60)
        
        old_xp = user.xp
        result = track_recipe_cooked(user, recipe, has_photo=True, has_rating=True)
        
        if result['success']:
            print(f"✅ Action tracked successfully!")
            print(f"   XP Gained: +{result['xp_result']['xp_gained']} (10 base + 5 photo + 3 rating)")
            print(f"   New XP: {result['xp_result']['new_xp']}")
            print(f"   New Level: {result['xp_result']['new_level']}")
        else:
            print(f"❌ Failed: {result['message']}")
        
        # Test 3: Get User Actions
        print("\n" + "-" * 60)
        print("TEST 3: Get User Actions (recent)")
        print("-" * 60)
        
        actions = get_user_actions(user, limit=5)
        print(f"Recent actions: {len(actions)}")
        for action in actions:
            print(f"  • {action.action_type}: +{action.xp_awarded} XP at {action.created_at}")
        
        # Test 4: Get Action Stats
        print("\n" + "-" * 60)
        print("TEST 4: Get Action Statistics")
        print("-" * 60)
        
        stats = get_action_stats(user)
        print(f"Total Actions: {stats['total_actions']}")
        print(f"Total XP Earned: {stats['total_xp_earned']}")
        print("\nBy Action Type:")
        for action_type, data in stats['by_type'].items():
            if data['count'] > 0:
                print(f"  {action_type:20s}: {data['count']:3d} actions, {data['xp_earned']:4d} XP")
        
        # Test 5: Get Recent Activity
        print("\n" + "-" * 60)
        print("TEST 5: Get Recent Activity (last 7 days)")
        print("-" * 60)
        
        activity = get_recent_activity(user, days=7, limit=5)
        print(f"Recent activity: {len(activity)} actions")
        for act in activity:
            print(f"  • {act['action_type']}: +{act['xp_awarded']} XP")
            if act['recipe_title']:
                print(f"    Recipe: {act['recipe_title']}")
        
        # Test 6: Refresh user data and show final stats
        print("\n" + "-" * 60)
        print("TEST 6: Final User Stats")
        print("-" * 60)
        
        user.reload()  # Refresh from database
        print(f"Final XP: {user.xp}")
        print(f"Final Level: {user.level} ({user.get_level_title()})")
        
        progress = user.get_xp_progress()
        print(f"Progress: {progress['xp_progress']}/{progress['next_level_xp'] - progress['current_level_xp']} ({progress['progress_percentage']}%)")
        print(f"XP to Next Level: {progress['xp_needed']}")
        
        print("\n" + "=" * 60)
        print("✅ ACTION TRACKING SYSTEM TEST COMPLETED!")
        print("=" * 60)
        print("\n⚠️  Note: Tests create real data in database.")
        print("Run test_cleanup.py to remove test actions if needed.")
        
    except User.DoesNotExist:
        print("\n❌ Test user 'testchef' not found")
        print("Please create a test user first.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_action_tracking()
