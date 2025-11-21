"""
Django management command to initialize default badges
"""
from django.core.management.base import BaseCommand
from apps.users.gamification import Badge


class Command(BaseCommand):
    help = 'Initialize default badges in the database'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating default badges...')
        
        badges = [
            {
                'name': 'First Recipe',
                'description': 'Created your first recipe',
                'icon': '🍳',
                'reward_xp': 50,
                'rarity': 'common',
                'criteria': {'recipes_submitted': 1}
            },
            {
                'name': 'Chef in Training',
                'description': 'Created 10 recipes',
                'icon': '👨‍🍳',
                'reward_xp': 200,
                'rarity': 'rare',
                'criteria': {'recipes_submitted': 10}
            },
            {
                'name': 'Master Chef',
                'description': 'Created 50 recipes',
                'icon': '🌟',
                'reward_xp': 1000,
                'rarity': 'epic',
                'criteria': {'recipes_submitted': 50}
            },
            {
                'name': 'Cooking Legend',
                'description': 'Created 100 recipes',
                'icon': '👑',
                'reward_xp': 5000,
                'rarity': 'legendary',
                'criteria': {'recipes_submitted': 100}
            },
            {
                'name': 'Social Butterfly',
                'description': 'Posted 100 comments',
                'icon': '💬',
                'reward_xp': 500,
                'rarity': 'rare',
                'criteria': {'comments_posted': 100}
            },
            {
                'name': 'Recipe Explorer',
                'description': 'Cooked 25 different recipes',
                'icon': '🔍',
                'reward_xp': 300,
                'rarity': 'rare',
                'criteria': {'recipes_cooked': 25}
            },
            {
                'name': 'Food Photographer',
                'description': 'Uploaded 50 photos',
                'icon': '📸',
                'reward_xp': 400,
                'rarity': 'rare',
                'criteria': {'photos_uploaded': 50}
            },
            {
                'name': 'Community Leader',
                'description': 'Gained 100 followers',
                'icon': '⭐',
                'reward_xp': 800,
                'rarity': 'epic',
                'criteria': {'followers': 100}
            },
            {
                'name': 'Early Adopter',
                'description': 'One of the first 100 users',
                'icon': '🎖️',
                'reward_xp': 100,
                'rarity': 'rare',
                'criteria': {'user_number': 100, 'operator': 'lte'}
            },
            {
                'name': 'Sharing is Caring',
                'description': 'Shared 50 recipes',
                'icon': '💝',
                'reward_xp': 250,
                'rarity': 'common',
                'criteria': {'recipes_shared': 50}
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for badge_data in badges:
            existing = Badge.objects(name=badge_data['name']).first()
            
            if existing:
                # Update existing badge
                for key, value in badge_data.items():
                    setattr(existing, key, value)
                existing.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated badge: {badge_data["name"]}')
                )
            else:
                # Create new badge
                Badge(**badge_data).save()
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created badge: {badge_data["name"]}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nDone! Created {created_count} new badges, updated {updated_count} existing badges.'
            )
        )
