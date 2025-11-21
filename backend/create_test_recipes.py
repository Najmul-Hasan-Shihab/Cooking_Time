"""
Create test recipes with full data for testing the recipe detail page
"""
import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.recipes.models import Recipe
from apps.users.gamification import Badge

# Get testchef user
user = User.objects(username='testchef').first()

if not user:
    print("❌ testchef user not found!")
    exit(1)

# Create a detailed recipe
recipe_data = {
    'title': 'Delicious Spaghetti Carbonara',
    'description': 'A classic Italian pasta dish made with eggs, cheese, bacon, and black pepper. Creamy, rich, and absolutely delicious!',
    'images': [
        'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=800'
    ],
    'ingredients': [
        {'name': 'Spaghetti', 'quantity': '400', 'unit': 'g'},
        {'name': 'Pancetta or Guanciale', 'quantity': '200', 'unit': 'g'},
        {'name': 'Egg Yolks', 'quantity': '4', 'unit': 'pieces'},
        {'name': 'Whole Eggs', 'quantity': '2', 'unit': 'pieces'},
        {'name': 'Pecorino Romano Cheese', 'quantity': '100', 'unit': 'g'},
        {'name': 'Black Pepper', 'quantity': '2', 'unit': 'tsp'},
        {'name': 'Salt', 'quantity': 'to taste', 'unit': ''},
    ],
    'steps': [
        {
            'step_number': 1,
            'text': 'Bring a large pot of salted water to a boil. Add spaghetti and cook according to package directions until al dente.',
            'step_time': 10
        },
        {
            'step_number': 2,
            'text': 'While pasta cooks, cut pancetta into small cubes. Cook in a large skillet over medium heat until crispy, about 5-7 minutes.',
            'step_time': 7
        },
        {
            'step_number': 3,
            'text': 'In a bowl, whisk together egg yolks, whole eggs, grated Pecorino Romano cheese, and plenty of black pepper.',
            'step_time': 3
        },
        {
            'step_number': 4,
            'text': 'Reserve 1 cup of pasta cooking water, then drain the spaghetti. Add hot pasta to the skillet with pancetta.',
            'step_time': 2
        },
        {
            'step_number': 5,
            'text': 'Remove from heat. Quickly pour in the egg mixture, tossing constantly. Add pasta water a little at a time until creamy.',
            'step_time': 3
        },
        {
            'step_number': 6,
            'text': 'Serve immediately with extra Pecorino Romano and black pepper on top. Enjoy!',
            'step_time': 1
        }
    ],
    'prep_time': 10,
    'cook_time': 15,
    'servings': 4,
    'difficulty': 'medium',
    'tags': ['pasta', 'italian', 'quick-meal', 'comfort-food'],
    'categories': ['Dinner', 'Main Course', 'Italian'],
    'cuisine': 'Italian',
    'nutrition': {
        'calories': 650,
        'protein': 28,
        'carbs': 75,
        'fat': 24,
        'fiber': 3,
        'sugar': 2
    },
    'rating_stats': {'average': 4.8, 'count': 127, 'total': 127},
    'views': 1542,
    'cook_count': 89,
    'rarity': 'rare',
    'is_published': True,
    'is_featured': False,
    'author': user
}

# Check if recipe already exists
existing = Recipe.objects(title=recipe_data['title']).first()
if existing:
    print(f"✅ Recipe '{recipe_data['title']}' already exists")
    print(f"   Slug: {existing.slug}")
    print(f"   URL: http://localhost:5173/recipes/{existing.slug}")
else:
    recipe = Recipe(**recipe_data)
    recipe.save()
    print(f"✅ Created recipe: {recipe.title}")
    print(f"   Slug: {recipe.slug}")
    print(f"   URL: http://localhost:5173/recipes/{recipe.slug}")

# Create another recipe
recipe_data_2 = {
    'title': 'Classic Margherita Pizza',
    'description': 'Authentic Neapolitan pizza with fresh mozzarella, tomatoes, and basil. Simple ingredients, amazing flavor!',
    'images': [
        'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800'
    ],
    'ingredients': [
        {'name': 'Pizza Dough', 'quantity': '500', 'unit': 'g'},
        {'name': 'San Marzano Tomatoes', 'quantity': '400', 'unit': 'g'},
        {'name': 'Fresh Mozzarella', 'quantity': '250', 'unit': 'g'},
        {'name': 'Fresh Basil Leaves', 'quantity': '20', 'unit': 'leaves'},
        {'name': 'Extra Virgin Olive Oil', 'quantity': '3', 'unit': 'tbsp'},
        {'name': 'Sea Salt', 'quantity': 'to taste', 'unit': ''},
    ],
    'steps': [
        {
            'step_number': 1,
            'text': 'Preheat your oven to the highest temperature (usually 500°F/260°C). If you have a pizza stone, place it in the oven.',
            'step_time': 30
        },
        {
            'step_number': 2,
            'text': 'Crush the San Marzano tomatoes by hand. Season with salt and a drizzle of olive oil. Set aside.',
            'step_time': 5
        },
        {
            'step_number': 3,
            'text': 'Stretch the pizza dough into a 12-inch circle on a floured surface. Make the edges slightly thicker.',
            'step_time': 5
        },
        {
            'step_number': 4,
            'text': 'Spread the tomato sauce on the dough, leaving a 1-inch border. Tear mozzarella and distribute evenly.',
            'step_time': 3
        },
        {
            'step_number': 5,
            'text': 'Transfer pizza to the preheated oven (or pizza stone). Bake for 8-12 minutes until crust is golden and cheese is bubbly.',
            'step_time': 10
        },
        {
            'step_number': 6,
            'text': 'Remove from oven, top with fresh basil leaves and a drizzle of olive oil. Slice and serve immediately!',
            'step_time': 2
        }
    ],
    'prep_time': 15,
    'cook_time': 40,
    'servings': 2,
    'difficulty': 'easy',
    'tags': ['pizza', 'italian', 'vegetarian', 'classic'],
    'categories': ['Dinner', 'Main Course', 'Italian', 'Vegetarian'],
    'cuisine': 'Italian',
    'nutrition': {
        'calories': 520,
        'protein': 22,
        'carbs': 65,
        'fat': 18,
        'fiber': 4,
        'sugar': 6
    },
    'rating_stats': {'average': 4.9, 'count': 203, 'total': 203},
    'views': 2341,
    'cook_count': 156,
    'rarity': 'common',
    'is_published': True,
    'is_featured': True,
    'author': user
}

existing_2 = Recipe.objects(title=recipe_data_2['title']).first()
if existing_2:
    print(f"\n✅ Recipe '{recipe_data_2['title']}' already exists")
    print(f"   Slug: {existing_2.slug}")
    print(f"   URL: http://localhost:5173/recipes/{existing_2.slug}")
else:
    recipe_2 = Recipe(**recipe_data_2)
    recipe_2.save()
    print(f"\n✅ Created recipe: {recipe_2.title}")
    print(f"   Slug: {recipe_2.slug}")
    print(f"   URL: http://localhost:5173/recipes/{recipe_2.slug}")

print("\n" + "="*60)
print("🎉 Test recipes ready!")
print("="*60)
