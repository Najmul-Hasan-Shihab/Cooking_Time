"""
URL patterns for user endpoints
"""
from django.urls import path
from . import views
from . import follow_views

urlpatterns = [
    # User stats by ID
    path('<str:user_id>/stats/', views.get_user_stats, name='user_stats'),
    
    # Current user stats
    path('me/stats/', views.get_current_user_stats, name='current_user_stats'),
    
    # User profile by username
    path('profile/<str:username>/', views.get_user_profile, name='user_profile'),
    
    # Update current user profile
    path('me/profile/', views.update_profile, name='update_profile'),
    
    # Following system
    path('<str:user_id>/follow/', follow_views.toggle_follow, name='toggle_follow'),
    path('<str:user_id>/followers/', follow_views.get_followers, name='get_followers'),
    path('<str:user_id>/following/', follow_views.get_following, name='get_following'),
    path('feed/', follow_views.get_activity_feed, name='activity_feed'),
]
