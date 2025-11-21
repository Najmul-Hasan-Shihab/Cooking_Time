"""
Recipe URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list_create, name='recipe-list-create'),
    path('search/', views.search_recipes, name='recipe-search'),
    path('<slug:slug>/', views.recipe_detail, name='recipe-detail'),
    path('<slug:slug>/mark_cooked/', views.mark_cooked, name='recipe-mark-cooked'),
]
