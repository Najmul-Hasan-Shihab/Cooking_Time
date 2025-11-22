"""
Cleanup script - Remove old user actions and fix user badges
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.gamification.models import UserAction

print("=" * 60)
print("DATABASE CLEANUP")
print("=" * 60)

# Drop user_actions collection to reset schema
print("\n1. Cleaning up UserActions...")
count = UserAction.objects.count()
if count > 0:
    UserAction.objects.delete()
    print(f"   ✅ Deleted {count} old user actions")
else:
    print("   ✅ No old user actions to delete")

# Fix user badges (convert to string list if needed)
print("\n2. Fixing user badges...")
users = User.objects.all()
for user in users:
    if user.badges and not all(isinstance(b, str) for b in user.badges):
        # Convert badges to empty list for now
        user.badges = []
        user.save()
        print(f"   ✅ Fixed badges for user: {user.username}")

print("\n" + "=" * 60)
print("✅ CLEANUP COMPLETED!")
print("=" * 60)
print("\nYou can now run test_action_tracker.py safely.")
