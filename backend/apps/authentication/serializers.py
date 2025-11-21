"""
Serializers for Authentication
"""
from rest_framework import serializers
from apps.users.models import User
import re


class UserRegistrationSerializer(serializers.Serializer):
    """Serializer for user registration"""
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    def validate_username(self, value):
        """Validate username"""
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, and underscores"
            )
        
        if User.objects(username=value).first():
            raise serializers.ValidationError("Username already exists")
        
        return value
    
    def validate_email(self, value):
        """Validate email"""
        if User.objects(email=value).first():
            raise serializers.ValidationError("Email already registered")
        
        return value
    
    def validate(self, data):
        """Validate password match"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                "password_confirm": "Passwords do not match"
            })
        
        return data
    
    def create(self, validated_data):
        """Create new user"""
        validated_data.pop('password_confirm')
        
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """Validate credentials"""
        username = data.get('username')
        password = data.get('password')
        
        user = User.objects(username=username).first()
        
        if not user or not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        
        data['user'] = user
        return data


class UserSerializer(serializers.Serializer):
    """Serializer for user data"""
    id = serializers.CharField(read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    avatar_url = serializers.URLField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True, max_length=500)
    xp = serializers.IntegerField(read_only=True)
    level = serializers.IntegerField(read_only=True)
    badges = serializers.ListField(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    preferences = serializers.DictField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    
    def to_representation(self, instance):
        """Convert User document to dict"""
        if isinstance(instance, User):
            return instance.to_dict()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password"""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """Validate passwords"""
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({
                "new_password_confirm": "Passwords do not match"
            })
        
        return data
