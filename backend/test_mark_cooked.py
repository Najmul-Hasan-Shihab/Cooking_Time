"""
Test script for Mark as Cooked endpoint
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
from apps.gamification.models import CookedRecipe
from apps.gamification.action_tracker import track_recipe_cooked
from apps.gamification.badge_engine import check_and_award_badges


def test_mark_cooked():
    """Test marking recipes as cooked"""
    print("=" * 60)
    print("MARK AS COOKED TEST")
    print("=" * 60)
    
    try:
        # Get test user
        user = User.objects.get(username='testchef')
        print(f"\n✅ Found user: {user.username}")
        print(f"Initial XP: {user.xp}")
        print(f"Initial Level: {user.level} ({user.get_level_title()})")
        print(f"Initial Badges: {len(user.badges)}")
        
        # Get a recipe to cook
        recipe = Recipe.objects(is_published=True).first()
        if not recipe:
            print("\n❌ No published recipes found")
            return
        
        print(f"\n📖 Recipe: {recipe.title}")
        print(f"Initial cook count: {recipe.cook_count}")
        
        # Test 1: Mark recipe as cooked (base)
        print("\n" + "-" * 60)
        print("TEST 1: Mark Recipe as Cooked (base - no photo/rating)")
        print("-" * 60)
        
        # Check if already cooked
        existing = CookedRecipe.objects(user=user, recipe=recipe).first()
        if existing:
            print(f"⚠️  Recipe already cooked. Deleting existing record...")
            existing.delete()
        
        # Track cooking action
        result = track_recipe_cooked(user, recipe, has_photo=False, has_rating=False)
        
        if result['success']:
            print(f"✅ Action tracked successfully!")
            print(f"   XP Gained: +{result['xp_result']['xp_gained']}")
            print(f"   New XP: {result['xp_result']['new_xp']}")
            print(f"   New Level: {result['xp_result']['new_level']}")
            
            # Create cooked recipe record
            cooked = CookedRecipe(user=user, recipe=recipe)
            cooked.save()
            print(f"   Cooked Record ID: {cooked.id}")
            
            # Increment cook count
            recipe.cook_count += 1
            recipe.save()
            print(f"   Recipe cook count: {recipe.cook_count}")
            
            # Check for badges
            badges = check_and_award_badges(user)
            if badges:
                print(f"\n   🎉 Earned {len(badges)} new badge(s)!")
                for badge in badges:
                    print(f"      {badge['icon']} {badge['name']}")
            else:
                print(f"   No new badges earned")
        else:
            print(f"❌ Failed: {result['message']}")
        
        # Test 2: Mark another recipe with photo and rating
        print("\n" + "-" * 60)
        print("TEST 2: Mark Recipe with Photo + Rating")
        print("-" * 60)
        
        # Get another recipe
        recipes = Recipe.objects(is_published=True).limit(2)
        if len(recipes) < 2:
            print("⚠️  Not enough recipes for this test")
        else:
            recipe2 = recipes[1]
            print(f"Recipe: {recipe2.title}")
            
            # Check if already cooked
            existing2 = CookedRecipe.objects(user=user, recipe=recipe2).first()
            if existing2:
                print(f"⚠️  Recipe already cooked. Deleting existing record...")
                existing2.delete()
            
            # Track with bonuses
            result2 = track_recipe_cooked(user, recipe2, has_photo=True, has_rating=True)
            
            if result2['success']:
                print(f"✅ Action tracked with bonuses!")
                print(f"   XP Gained: +{result2['xp_result']['xp_gained']} (10 base + 5 photo + 3 rating)")
                print(f"   New XP: {result2['xp_result']['new_xp']}")
                
                # Create cooked recipe with data
                cooked2 = CookedRecipe(
                    user=user,
                    recipe=recipe2,
                    photo_url="https://example.com/my-cooked-photo.jpg",
                    rating=4.5,
                    notes="Turned out great!"
                )
                cooked2.save()
                print(f"   Photo: {cooked2.photo_url}")
                print(f"   Rating: {cooked2.rating}/5.0")
                print(f"   Notes: {cooked2.notes}")
                
                # Update recipe stats
                recipe2.cook_count += 1
                recipe2.rating_stats.count += 1
                recipe2.rating_stats.total += cooked2.rating
                recipe2.rating_stats.average = recipe2.rating_stats.total / recipe2.rating_stats.count
                recipe2.save()
                
                print(f"   Recipe cook count: {recipe2.cook_count}")
                print(f"   Recipe avg rating: {recipe2.rating_stats.average:.2f} ({recipe2.rating_stats.count} ratings)")
                
                # Check badges again
                badges2 = check_and_award_badges(user)
                if badges2:
                    print(f"\n   🎉 Earned {len(badges2)} new badge(s)!")
                    for badge in badges2:
                        print(f"      {badge['icon']} {badge['name']}")
        
        # Test 3: Query cooked recipes
        print("\n" + "-" * 60)
        print("TEST 3: Query User's Cooked Recipes")
        print("-" * 60)
        
        cooked_recipes = CookedRecipe.objects(user=user)
        print(f"Total recipes cooked: {cooked_recipes.count()}")
        
        for cooked in cooked_recipes:
            print(f"\n  • {cooked.recipe.title}")
            print(f"    Cooked at: {cooked.cooked_at}")
            if cooked.rating:
                print(f"    Rating: {cooked.rating}/5.0")
            if cooked.photo_url:
                print(f"    Photo: {cooked.photo_url}")
            if cooked.notes:
                print(f"    Notes: {cooked.notes}")
        
        # Test 4: Final Stats
        print("\n" + "-" * 60)
        print("TEST 4: Final User Stats")
        print("-" * 60)
        
        user.reload()
        print(f"Final XP: {user.xp}")
        print(f"Final Level: {user.level} ({user.get_level_title()})")
        print(f"Total Badges: {len(user.badges)}")
        print(f"Total Recipes Cooked: {CookedRecipe.objects(user=user).count()}")
        
        progress = user.get_xp_progress()
        print(f"XP Progress: {progress['xp_progress']}/{progress['next_level_xp'] - progress['current_level_xp']} ({progress['progress_percentage']:.2f}%)")
        
        print("\n" + "=" * 60)
        print("✅ MARK AS COOKED TEST COMPLETED!")
        print("=" * 60)
        
    except User.DoesNotExist:
        print("\n❌ Test user 'testchef' not found")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_mark_cooked()
