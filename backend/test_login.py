"""
Quick test script to verify testchef user and password
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.users.gamification import Badge
from apps.recipes.models import Recipe

# Test the user
username = 'testchef'
password = 'password123'

print(f"\n🔍 Testing user: {username}")
print("="*50)

user = User.objects(username=username).first()

if not user:
    print(f"❌ User '{username}' NOT FOUND in database!")
    print("\n📋 All users in database:")
    for u in User.objects.all():
        print(f"  - {u.username} ({u.email})")
else:
    print(f"✅ User FOUND: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Active: {user.is_active}")
    print(f"   Level: {user.level}")
    print(f"   XP: {user.xp}")
    
    # Test password
    print(f"\n🔐 Testing password...")
    if user.check_password(password):
        print(f"✅ Password is CORRECT!")
    else:
        print(f"❌ Password is WRONG!")
        print(f"   Hash in DB: {user.password_hash[:50]}...")

print("\n" + "="*50)
