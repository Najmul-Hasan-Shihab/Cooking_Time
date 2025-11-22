"""
Recipe URLs
"""
from django.urls import path
from . import views
from apps.gamification import comments_views, saved_recipes_views

urlpatterns = [
    path('', views.recipe_list_create, name='recipe-list-create'),
    path('search/', views.search_recipes, name='recipe-search'),
    path('saved/', saved_recipes_views.list_saved_recipes, name='recipe-list-saved'),
    path('cooked/', saved_recipes_views.list_cooked_recipes, name='recipe-list-cooked'),
    path('<slug:slug>/', views.recipe_detail, name='recipe-detail'),
    path('<slug:slug>/mark_cooked/', views.mark_cooked, name='recipe-mark-cooked'),
    path('<slug:slug>/save/', saved_recipes_views.toggle_save_recipe, name='recipe-toggle-save'),
    
    # Comment endpoints
    path('<slug:slug>/comments/', comments_views.comments_list_create, name='recipe-comments'),
]
