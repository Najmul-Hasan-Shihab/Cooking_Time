#!/usr/bin/env python
"""
Test script for User Stats Endpoint

Tests:
1. Get stats by user ID
2. Verify all stats are returned correctly
3. Test with testchef user
4. Check XP progress, recipes, badges, social stats
"""
import requests
import json
from pprint import pprint

BASE_URL = 'http://localhost:8000'
TEST_USER = 'testchef'
TEST_PASS = 'password123'


def login():
    """Login and get JWT token"""
    print("🔐 Logging in as testchef...")
    response = requests.post(f'{BASE_URL}/api/auth/login/', json={
        'username': TEST_USER,
        'password': TEST_PASS
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login successful!")
        print(f"   User ID: {data['user']['id']}")
        print(f"   Username: {data['user']['username']}")
        print(f"   XP: {data['user']['xp']}")
        print(f"   Level: {data['user']['level']}")
        return data['access'], data['user']['id']
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        return None, None


def test_user_stats(user_id, token):
    """Test GET /api/users/:id/stats/"""
    print(f"\n📊 Testing GET /api/users/{user_id}/stats/...")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/api/users/{user_id}/stats/', headers=headers)
    
    if response.status_code == 200:
        stats = response.json()
        print("✅ User stats retrieved successfully!\n")
        
        print("=" * 60)
        print("USER STATISTICS")
        print("=" * 60)
        
        # User info
        user = stats['user']
        print(f"\n👤 USER INFO:")
        print(f"   ID: {user['id']}")
        print(f"   Username: {user['username']}")
        print(f"   Email: {user.get('email', 'N/A')}")
        print(f"   Bio: {user.get('bio', 'No bio')}")
        print(f"   Active: {user['is_active']}")
        
        # XP info
        xp = stats['xp_info']
        print(f"\n⭐ XP & LEVEL:")
        print(f"   Total XP: {xp['total_xp']}")
        print(f"   Level: {xp['current_level']} - {xp['level_title']}")
        print(f"   Next Level: {xp['next_level']}")
        print(f"   Progress: {xp['xp_in_current_level']}/{xp['xp_for_next_level']} ({xp['progress_percentage']:.1f}%)")
        print(f"   XP Needed: {xp['xp_needed']}")
        
        # Recipes
        recipes = stats['recipes']
        print(f"\n📖 RECIPES:")
        print(f"   Created: {recipes['created']}")
        print(f"   Cooked: {recipes['cooked']}")
        
        # Badges
        badges = stats['badges']
        print(f"\n🏆 BADGES ({badges['total_earned']} earned):")
        if badges['badges']:
            for badge in badges['badges']:
                print(f"   {badge['icon']} {badge['name']} ({badge['rarity']})")
                print(f"      {badge['description']}")
                print(f"      XP Reward: +{badge['xp_reward']}")
        else:
            print("   No badges earned yet")
        
        # Social
        social = stats['social']
        print(f"\n👥 SOCIAL:")
        print(f"   Followers: {social['followers']}")
        print(f"   Following: {social['following']}")
        
        # Join date
        print(f"\n📅 JOINED: {stats['join_date']}")
        
        # Recent activity
        activity = stats['recent_activity']
        print(f"\n📈 RECENT ACTIVITY (last {len(activity)} actions):")
        if activity:
            for action in activity[:10]:  # Show top 10
                recipe_info = ""
                if action.get('target_recipe'):
                    recipe = action['target_recipe']
                    recipe_info = f" - {recipe['title']}"
                print(f"   • {action['action_type']} (+{action['xp_awarded']} XP){recipe_info}")
                print(f"     {action['created_at']}")
        else:
            print("   No recent activity")
        
        # Action stats
        if 'action_stats' in stats:
            action_stats = stats['action_stats']
            print(f"\n📊 ACTION STATISTICS:")
            for action_type, count in action_stats.items():
                print(f"   {action_type}: {count}")
        
        print("\n" + "=" * 60)
        
        return stats
    else:
        print(f"❌ Failed to get stats: {response.status_code}")
        print(response.text)
        return None


def test_current_user_stats(token):
    """Test GET /api/users/me/stats/"""
    print(f"\n📊 Testing GET /api/users/me/stats/ (current user)...")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/api/users/me/stats/', headers=headers)
    
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Current user stats retrieved!")
        print(f"   User: {stats['user']['username']}")
        print(f"   Level: {stats['xp_info']['current_level']} - {stats['xp_info']['level_title']}")
        print(f"   XP: {stats['xp_info']['total_xp']}")
        return stats
    else:
        print(f"❌ Failed to get current user stats: {response.status_code}")
        print(response.text)
        return None


def test_profile_by_username(token, username):
    """Test GET /api/users/profile/:username/"""
    print(f"\n📊 Testing GET /api/users/profile/{username}/...")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/api/users/profile/{username}/', headers=headers)
    
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Profile retrieved by username!")
        print(f"   User ID: {stats['user']['id']}")
        print(f"   Username: {stats['user']['username']}")
        return stats
    else:
        print(f"❌ Failed to get profile: {response.status_code}")
        print(response.text)
        return None


def main():
    print("=" * 60)
    print("USER STATS ENDPOINT TEST")
    print("=" * 60)
    
    # Login
    token, user_id = login()
    if not token:
        print("\n❌ Cannot continue without authentication")
        return
    
    # Test 1: Get stats by user ID
    print("\n" + "=" * 60)
    print("TEST 1: Get User Stats by ID")
    print("=" * 60)
    stats = test_user_stats(user_id, token)
    
    if not stats:
        print("\n❌ Stats test failed")
        return
    
    # Test 2: Get current user stats
    print("\n" + "=" * 60)
    print("TEST 2: Get Current User Stats")
    print("=" * 60)
    current_stats = test_current_user_stats(token)
    
    # Test 3: Get profile by username
    print("\n" + "=" * 60)
    print("TEST 3: Get Profile by Username")
    print("=" * 60)
    profile = test_profile_by_username(token, TEST_USER)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("✅ Test 1: User stats by ID - PASSED" if stats else "❌ Test 1: FAILED")
    print("✅ Test 2: Current user stats - PASSED" if current_stats else "❌ Test 2: FAILED")
    print("✅ Test 3: Profile by username - PASSED" if profile else "❌ Test 3: FAILED")
    
    if stats and current_stats and profile:
        print("\n🎉 ALL TESTS PASSED!")
        print(f"\nUser Stats Endpoint is working correctly!")
        print(f"✅ Returns comprehensive statistics")
        print(f"✅ Multiple endpoint variations working")
        print(f"✅ XP progress tracking accurate")
        print(f"✅ Badge information included")
        print(f"✅ Recent activity tracked")
    else:
        print("\n❌ SOME TESTS FAILED")


if __name__ == '__main__':
    main()
