"""
Reset testchef password to password123
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.users.gamification import Badge
from apps.recipes.models import Recipe

# Get the user
user = User.objects(username='testchef').first()

if user:
    print(f"\n🔧 Resetting password for: {user.username}")
    print("="*50)
    
    # Set new password
    user.set_password('password123')
    user.save()
    
    print(f"✅ Password reset successful!")
    print(f"\n🔐 Testing new password...")
    
    # Test it
    user = User.objects(username='testchef').first()
    if user.check_password('password123'):
        print(f"✅ Password verification PASSED!")
        print(f"\n📋 Login credentials:")
        print(f"   Username: testchef")
        print(f"   Password: password123")
    else:
        print(f"❌ Password verification FAILED!")
    
    print("="*50)
else:
    print("❌ User 'testchef' not found!")
