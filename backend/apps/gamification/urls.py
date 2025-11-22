"""
URL patterns for gamification app
"""
from django.urls import path
from . import views, comments_views

app_name = 'gamification'

urlpatterns = [
    # Badge endpoints
    path('badges/', views.get_all_badges, name='badges-list'),
    path('badges/initialize/', views.initialize_badges, name='badges-initialize'),
    path('badges/progress/', views.get_badge_progress_view, name='badges-progress'),
    path('badges/check/', views.check_badges_view, name='badges-check'),
    path('users/<str:user_id>/badges/', views.get_user_badges_view, name='user-badges'),
]
