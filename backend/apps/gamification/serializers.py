"""
Serializers for gamification models
"""
from rest_framework import serializers


class BadgeSerializer(serializers.Serializer):
    """Serializer for Badge model"""
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    icon = serializers.CharField()
    criteria_type = serializers.CharField()
    criteria_value = serializers.IntegerField()
    rarity = serializers.CharField()
    xp_reward = serializers.IntegerField()


class UserActionSerializer(serializers.Serializer):
    """Serializer for UserAction model"""
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField()
    action_type = serializers.CharField()
    target_recipe_id = serializers.CharField(allow_null=True)
    xp_awarded = serializers.IntegerField()
    metadata = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)


class CookedRecipeSerializer(serializers.Serializer):
    """Serializer for CookedRecipe model"""
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField()
    recipe_id = serializers.CharField()
    recipe_title = serializers.CharField(read_only=True)
    photo_url = serializers.CharField(allow_null=True, allow_blank=True)
    rating = serializers.FloatField(allow_null=True, min_value=1.0, max_value=5.0)
    notes = serializers.CharField(allow_null=True, allow_blank=True)
    cooked_at = serializers.DateTimeField(read_only=True)


class BadgeProgressSerializer(serializers.Serializer):
    """Serializer for badge progress"""
    badge = BadgeSerializer()
    current_value = serializers.IntegerField()
    required_value = serializers.IntegerField()
    percentage = serializers.FloatField()
    earned = serializers.BooleanField()


class XPGainSerializer(serializers.Serializer):
    """Serializer for XP gain result"""
    xp_gained = serializers.IntegerField()
    new_xp = serializers.IntegerField()
    old_level = serializers.IntegerField()
    new_level = serializers.IntegerField()
    level_up = serializers.DictField(allow_null=True)
    action_type = serializers.CharField(allow_null=True)
    badges_earned = serializers.ListField(child=BadgeSerializer(), allow_null=True)
