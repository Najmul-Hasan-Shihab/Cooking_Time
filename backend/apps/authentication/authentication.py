"""
Custom JWT Authentication for MongoEngine
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from apps.users.models import User


class MongoEngineJWTAuthentication(JWTAuthentication):
    """Custom JWT Authentication that works with MongoEngine"""
    
    def get_user(self, validated_token):
        """
        Get user from MongoDB using user_id from token
        """
        try:
            user_id = validated_token.get('user_id')
            if not user_id:
                raise exceptions.AuthenticationFailed('Token contained no recognizable user identification')
            
            user = User.objects(id=user_id).first()
            
            if not user:
                raise exceptions.AuthenticationFailed('User not found')
            
            if not user.is_active:
                raise exceptions.AuthenticationFailed('User is inactive')
            
            return user
            
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Authentication failed: {str(e)}')


class MongoEngineJWTAuthenticationMiddleware:
    """Middleware to add user_id to request from JWT token"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = MongoEngineJWTAuthentication()
    
    def __call__(self, request):
        # Try to authenticate using JWT
        try:
            auth_result = self.jwt_auth.authenticate(request)
            if auth_result:
                user, token = auth_result
                request.user_id = str(user.id)
                request.mongo_user = user
        except:
            pass
        
        response = self.get_response(request)
        return response
