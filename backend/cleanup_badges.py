"""
Cleanup badges collection
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.gamification.models import Badge

print("=" * 60)
print("CLEANING UP BADGES")
print("=" * 60)

count = Badge.objects.count()
if count > 0:
    Badge.objects.delete()
    print(f"✅ Deleted {count} old badges")
else:
    print("✅ No old badges to delete")

print("\nYou can now run test_badge_engine.py to create fresh badges.")
