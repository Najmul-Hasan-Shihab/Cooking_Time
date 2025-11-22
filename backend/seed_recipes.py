"""
Seed database with 10 diverse recipes
"""
import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.recipes.models import Recipe

# Get testchef user
user = User.objects(username='testchef').first()

if not user:
    print("❌ testchef user not found!")
    exit(1)

recipes = [
    {
        'title': 'Thai Green Curry',
        'description': 'Aromatic and spicy Thai curry with coconut milk, vegetables, and tender chicken. A perfect balance of sweet, salty, and spicy flavors.',
        'images': ['https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=800'],
        'ingredients': [
            {'name': 'Chicken Breast', 'quantity': '500', 'unit': 'g'},
            {'name': 'Green Curry Paste', 'quantity': '3', 'unit': 'tbsp'},
            {'name': 'Coconut Milk', 'quantity': '400', 'unit': 'ml'},
            {'name': 'Thai Basil', 'quantity': '1', 'unit': 'cup'},
            {'name': 'Bell Peppers', 'quantity': '2', 'unit': 'pieces'},
            {'name': 'Bamboo Shoots', 'quantity': '200', 'unit': 'g'},
            {'name': 'Fish Sauce', 'quantity': '2', 'unit': 'tbsp'},
            {'name': 'Palm Sugar', 'quantity': '1', 'unit': 'tbsp'},
        ],
        'steps': [
            {'step_number': 1, 'text': 'Heat oil in a wok over medium heat. Add curry paste and fry until fragrant, about 2 minutes.', 'step_time': 3},
            {'step_number': 2, 'text': 'Add half the coconut milk and stir until well combined with the paste.', 'step_time': 2},
            {'step_number': 3, 'text': 'Add chicken pieces and cook until they turn white, about 5 minutes.', 'step_time': 5},
            {'step_number': 4, 'text': 'Add remaining coconut milk, vegetables, fish sauce, and palm sugar. Simmer for 10 minutes.', 'step_time': 10},
            {'step_number': 5, 'text': 'Add Thai basil leaves and stir. Serve hot with jasmine rice.', 'step_time': 2},
        ],
        'prep_time': 15,
        'cook_time': 20,
        'servings': 4,
        'difficulty': 'medium',
        'tags': ['thai', 'curry', 'spicy', 'asian'],
        'categories': ['Dinner', 'Main Course', 'Thai'],
        'cuisine': 'Thai',
        'nutrition': {'calories': 420, 'protein': 32, 'carbs': 18, 'fat': 26, 'fiber': 3, 'sugar': 8},
        'rating_stats': {'average': 4.7, 'count': 89, 'total': 89},
        'views': 1234,
        'cook_count': 67,
        'rarity': 'rare',
        'is_published': True,
        'is_featured': False,
        'author': user
    },
    {
        'title': 'Classic Beef Tacos',
        'description': 'Authentic Mexican street tacos with seasoned ground beef, fresh toppings, and homemade salsa. Quick, easy, and delicious!',
        'images': ['https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800'],
        'ingredients': [
            {'name': 'Ground Beef', 'quantity': '500', 'unit': 'g'},
            {'name': 'Taco Seasoning', 'quantity': '2', 'unit': 'tbsp'},
            {'name': 'Corn Tortillas', 'quantity': '12', 'unit': 'pieces'},
            {'name': 'Lettuce', 'quantity': '2', 'unit': 'cups'},
            {'name': 'Tomatoes', 'quantity': '3', 'unit': 'pieces'},
            {'name': 'Cheddar Cheese', 'quantity': '200', 'unit': 'g'},
            {'name': 'Sour Cream', 'quantity': '150', 'unit': 'ml'},
            {'name': 'Lime', 'quantity': '2', 'unit': 'pieces'},
        ],
        'steps': [
            {'step_number': 1, 'text': 'Brown ground beef in a large skillet over medium-high heat, breaking it up as it cooks.', 'step_time': 8},
            {'step_number': 2, 'text': 'Add taco seasoning and 1/2 cup water. Simmer until liquid evaporates, about 5 minutes.', 'step_time': 5},
            {'step_number': 3, 'text': 'Warm tortillas in a dry skillet or microwave until pliable.', 'step_time': 3},
            {'step_number': 4, 'text': 'Chop lettuce and tomatoes. Shred cheese if needed.', 'step_time': 5},
            {'step_number': 5, 'text': 'Assemble tacos with beef, lettuce, tomatoes, cheese, and sour cream. Squeeze lime over top.', 'step_time': 4},
        ],
        'prep_time': 10,
        'cook_time': 15,
        'servings': 4,
        'difficulty': 'easy',
        'tags': ['mexican', 'tacos', 'quick-meal', 'family-friendly'],
        'categories': ['Dinner', 'Main Course', 'Mexican'],
        'cuisine': 'Mexican',
        'nutrition': {'calories': 480, 'protein': 28, 'carbs': 35, 'fat': 24, 'fiber': 5, 'sugar': 3},
        'rating_stats': {'average': 4.6, 'count': 156, 'total': 156},
        'views': 2890,
        'cook_count': 124,
        'rarity': 'common',
        'is_published': True,
        'is_featured': True,
        'author': user
    },
    {
        'title': 'Japanese Chicken Teriyaki',
        'description': 'Tender chicken glazed with homemade teriyaki sauce. Sweet, savory, and incredibly satisfying served over steamed rice.',
        'images': ['https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=800'],
        'ingredients': [
            {'name': 'Chicken Thighs', 'quantity': '600', 'unit': 'g'},
            {'name': 'Soy Sauce', 'quantity': '4', 'unit': 'tbsp'},
            {'name': 'Mirin', 'quantity': '3', 'unit': 'tbsp'},
            {'name': 'Sake', 'quantity': '2', 'unit': 'tbsp'},
            {'name': 'Sugar', 'quantity': '2', 'unit': 'tbsp'},
            {'name': 'Ginger', 'quantity': '1', 'unit': 'inch'},
            {'name': 'Garlic', 'quantity': '3', 'unit': 'cloves'},
            {'name': 'Sesame Seeds', 'quantity': '1', 'unit': 'tbsp'},
            {'name': 'Green Onions', 'quantity': '3', 'unit': 'stalks'},
        ],
        'steps': [
            {'step_number': 1, 'text': 'Mix soy sauce, mirin, sake, and sugar in a bowl to make teriyaki sauce.', 'step_time': 3},
            {'step_number': 2, 'text': 'Mince ginger and garlic. Heat oil in a pan and sauté until fragrant.', 'step_time': 3},
            {'step_number': 3, 'text': 'Add chicken thighs skin-side down. Cook until golden brown, about 6 minutes per side.', 'step_time': 12},
            {'step_number': 4, 'text': 'Pour teriyaki sauce over chicken. Simmer until sauce thickens and chicken is glazed, about 5 minutes.', 'step_time': 5},
            {'step_number': 5, 'text': 'Slice chicken, garnish with sesame seeds and green onions. Serve with steamed rice.', 'step_time': 3},
        ],
        'prep_time': 10,
        'cook_time': 25,
        'servings': 3,
        'difficulty': 'easy',
        'tags': ['japanese', 'chicken', 'teriyaki', 'asian'],
        'categories': ['Dinner', 'Main Course', 'Japanese'],
        'cuisine': 'Japanese',
        'nutrition': {'calories': 380, 'protein': 35, 'carbs': 22, 'fat': 16, 'fiber': 1, 'sugar': 14},
        'rating_stats': {'average': 4.8, 'count': 178, 'total': 178},
        'views': 3245,
        'cook_count': 142,
        'rarity': 'common',
        'is_published': True,
        'is_featured': True,
        'author': user
    },
    {
        'title': 'Mediterranean Quinoa Salad',
        'description': 'Fresh and healthy quinoa salad loaded with Mediterranean vegetables, feta cheese, and a zesty lemon dressing. Perfect for meal prep!',
        'images': ['https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?w=800'],
        'ingredients': [
            {'name': 'Quinoa', 'quantity': '1', 'unit': 'cup'},
            {'name': 'Cherry Tomatoes', 'quantity': '2', 'unit': 'cups'},
            {'name': 'Cucumber', 'quantity': '1', 'unit': 'large'},
            {'name': 'Red Onion', 'quantity': '1', 'unit': 'small'},
            {'name': 'Feta Cheese', 'quantity': '150', 'unit': 'g'},
            {'name': 'Kalamata Olives', 'quantity': '1', 'unit': 'cup'},
            {'name': 'Lemon Juice', 'quantity': '3', 'unit': 'tbsp'},
            {'name': 'Olive Oil', 'quantity': '4', 'unit': 'tbsp'},
            {'name': 'Fresh Parsley', 'quantity': '1/2', 'unit': 'cup'},
        ],
        'steps': [
            {'step_number': 1, 'text': 'Rinse quinoa and cook according to package directions. Let cool completely.', 'step_time': 20},
            {'step_number': 2, 'text': 'Chop tomatoes, cucumber, and red onion. Crumble feta cheese.', 'step_time': 10},
            {'step_number': 3, 'text': 'In a large bowl, combine cooled quinoa, vegetables, olives, and feta.', 'step_time': 5},
            {'step_number': 4, 'text': 'Whisk together lemon juice, olive oil, salt, and pepper for the dressing.', 'step_time': 3},
            {'step_number': 5, 'text': 'Pour dressing over salad, add parsley, and toss well. Refrigerate for 30 minutes before serving.', 'step_time': 5},
        ],
        'prep_time': 15,
        'cook_time': 20,
        'servings': 6,
        'difficulty': 'easy',
        'tags': ['salad', 'healthy', 'vegetarian', 'mediterranean', 'meal-prep'],
        'categories': ['Lunch', 'Salad', 'Vegetarian', 'Healthy'],
        'cuisine': 'Mediterranean',
        'nutrition': {'calories': 280, 'protein': 9, 'carbs': 28, 'fat': 15, 'fiber': 4, 'sugar': 3},
        'rating_stats': {'average': 4.5, 'count': 92, 'total': 92},
        'views': 1567,
        'cook_count': 78,
        'rarity': 'common',
        'is_published': True,
        'is_featured': False,
        'author': user
    },
    {
        'title': 'French Onion Soup',
        'description': 'Classic French comfort food with caramelized onions, rich beef broth, and melted Gruyère cheese on top. Elegant and warming!',
        'images': ['https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800'],
        'ingredients': [
            {'name': 'Yellow Onions', 'quantity': '6', 'unit': 'large'},
            {'name': 'Butter', 'quantity': '4', 'unit': 'tbsp'},
            {'name': 'Beef Broth', 'quantity': '8', 'unit': 'cups'},
            {'name': 'White Wine', 'quantity': '1', 'unit': 'cup'},
            {'name': 'Bay Leaves', 'quantity': '2', 'unit': 'pieces'},
            {'name': 'Thyme', 'quantity': '1', 'unit': 'tsp'},
            {'name': 'French Bread', 'quantity': '8', 'unit': 'slices'},
            {'name': 'Gruyère Cheese', 'quantity': '300', 'unit': 'g'},
        ],
        'steps': [
            {'step_number': 1, 'text': 'Slice onions thinly. Melt butter in a large pot and add onions with a pinch of salt.', 'step_time': 10},
            {'step_number': 2, 'text': 'Cook onions over medium-low heat, stirring occasionally, until deeply caramelized, about 45 minutes.', 'step_time': 45},
            {'step_number': 3, 'text': 'Add white wine and scrape up any brown bits. Cook until wine reduces by half.', 'step_time': 5},
            {'step_number': 4, 'text': 'Add beef broth, bay leaves, and thyme. Simmer for 30 minutes.', 'step_time': 30},
            {'step_number': 5, 'text': 'Toast bread slices. Ladle soup into oven-safe bowls, top with bread and cheese. Broil until bubbly.', 'step_time': 5},
        ],
        'prep_time': 15,
        'cook_time': 85,
        'servings': 6,
        'difficulty': 'medium',
        'tags': ['french', 'soup', 'comfort-food', 'winter'],
        'categories': ['Dinner', 'Soup', 'French'],
        'cuisine': 'French',
        'nutrition': {'calories': 380, 'protein': 18, 'carbs': 36, 'fat': 18, 'fiber': 4, 'sugar': 12},
        'rating_stats': {'average': 4.9, 'count': 134, 'total': 134},
        'views': 2456,
        'cook_count': 98,
        'rarity': 'rare',
        'is_published': True,
        'is_featured': True,
        'author': user
    },
    {
        'title': 'Korean Bibimbap',
        'description': 'Colorful Korean rice bowl with assorted vegetables, marinated beef, fried egg, and spicy gochujang sauce. A complete meal in one bowl!',
        'images': ['https://images.unsplash.com/photo-1553163147-622ab57be1c7?w=800'],
        'ingredients': [
            {'name': 'Short Grain Rice', 'quantity': '3', 'unit': 'cups'},
            {'name': 'Beef Sirloin', 'quantity': '300', 'unit': 'g'},
            {'name': 'Spinach', 'quantity': '200', 'unit': 'g'},
            {'name': 'Bean Sprouts', 'quantity': '200', 'unit': 'g'},
            {'name': 'Carrots', 'quantity': '2', 'unit': 'medium'},
            {'name': 'Zucchini', 'quantity': '1', 'unit': 'medium'},
            {'name': 'Shiitake Mushrooms', 'quantity': '150', 'unit': 'g'},
            {'name': 'Eggs', 'quantity': '4', 'unit': 'pieces'},
            {'name': 'Gochujang', 'quantity': '4', 'unit': 'tbsp'},
            {'name': 'Sesame Oil', 'quantity': '3', 'unit': 'tbsp'},
        ],
        'steps': [
            {'step_number': 1, 'text': 'Cook rice according to package directions. Keep warm.', 'step_time': 20},
            {'step_number': 2, 'text': 'Marinate thinly sliced beef in soy sauce, sesame oil, and garlic for 15 minutes. Cook in hot pan.', 'step_time': 20},
            {'step_number': 3, 'text': 'Blanch spinach and bean sprouts separately. Squeeze out excess water and season with sesame oil.', 'step_time': 10},
            {'step_number': 4, 'text': 'Julienne carrots and zucchini. Stir-fry separately until tender. Sauté mushrooms with garlic.', 'step_time': 15},
            {'step_number': 5, 'text': 'Fry eggs sunny-side up. Assemble bowls with rice, arrange vegetables and beef on top, add egg and gochujang.', 'step_time': 10},
        ],
        'prep_time': 25,
        'cook_time': 40,
        'servings': 4,
        'difficulty': 'medium',
        'tags': ['korean', 'rice-bowl', 'healthy', 'colorful'],
        'categories': ['Dinner', 'Main Course', 'Korean'],
        'cuisine': 'Korean',
        'nutrition': {'calories': 580, 'protein': 28, 'carbs': 72, 'fat': 18, 'fiber': 6, 'sugar': 8},
        'rating_stats': {'average': 4.8, 'count': 167, 'total': 167},
        'views': 2987,
        'cook_count': 135,
        'rarity': 'rare',
        'is_published': True,
        'is_featured': True,
        'author': user
    },
    {
        'title': 'Chocolate Lava Cake',
        'description': 'Decadent individual chocolate cakes with a molten chocolate center. The ultimate dessert for chocolate lovers!',
        'images': ['https://images.unsplash.com/photo-1624353365286-3f8d62daad51?w=800'],
        'ingredients': [
            {'name': 'Dark Chocolate', 'quantity': '200', 'unit': 'g'},
            {'name': 'Butter', 'quantity': '100', 'unit': 'g'},
            {'name': 'Eggs', 'quantity': '3', 'unit': 'pieces'},
            {'name': 'Egg Yolks', 'quantity': '3', 'unit': 'pieces'},
            {'name': 'Sugar', 'quantity': '100', 'unit': 'g'},
            {'name': 'All-Purpose Flour', 'quantity': '60', 'unit': 'g'},
            {'name': 'Vanilla Extract', 'quantity': '1', 'unit': 'tsp'},
            {'name': 'Salt', 'quantity': '1/4', 'unit': 'tsp'},
        ],
        'steps': [
            {'step_number': 1, 'text': 'Preheat oven to 425°F (220°C). Butter and flour 6 ramekins.', 'step_time': 5},
            {'step_number': 2, 'text': 'Melt chocolate and butter together in a double boiler or microwave. Stir until smooth.', 'step_time': 5},
            {'step_number': 3, 'text': 'Whisk eggs, egg yolks, and sugar until thick and pale. Add vanilla.', 'step_time': 5},
            {'step_number': 4, 'text': 'Fold chocolate mixture into eggs. Sift in flour and salt, fold gently until just combined.', 'step_time': 3},
            {'step_number': 5, 'text': 'Divide batter among ramekins. Bake for 12-14 minutes until edges are firm but center jiggles. Invert onto plates immediately.', 'step_time': 14},
        ],
        'prep_time': 15,
        'cook_time': 14,
        'servings': 6,
        'difficulty': 'medium',
        'tags': ['dessert', 'chocolate', 'romantic', 'french'],
        'categories': ['Dessert', 'French', 'Chocolate'],
        'cuisine': 'French',
        'nutrition': {'calories': 420, 'protein': 8, 'carbs': 38, 'fat': 28, 'fiber': 3, 'sugar': 28},
        'rating_stats': {'average': 4.9, 'count': 245, 'total': 245},
        'views': 4521,
        'cook_count': 189,
        'rarity': 'legendary',
        'is_published': True,
        'is_featured': True,
        'author': user
    },
    {
        'title': 'Indian Butter Chicken',
        'description': 'Rich and creamy North Indian curry with tender chicken in a tomato-based sauce. Best served with naan or basmati rice!',
        'images': ['https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=800'],
        'ingredients': [
            {'name': 'Chicken Breast', 'quantity': '700', 'unit': 'g'},
            {'name': 'Yogurt', 'quantity': '200', 'unit': 'ml'},
            {'name': 'Tomato Puree', 'quantity': '400', 'unit': 'g'},
            {'name': 'Heavy Cream', 'quantity': '200', 'unit': 'ml'},
            {'name': 'Butter', 'quantity': '100', 'unit': 'g'},
            {'name': 'Garam Masala', 'quantity': '2', 'unit': 'tbsp'},
            {'name': 'Ginger-Garlic Paste', 'quantity': '2', 'unit': 'tbsp'},
            {'name': 'Kashmiri Chili Powder', 'quantity': '1', 'unit': 'tbsp'},
            {'name': 'Fenugreek Leaves', 'quantity': '1', 'unit': 'tbsp'},
        ],
        'steps': [
            {'step_number': 1, 'text': 'Marinate chicken in yogurt, garam masala, and salt for at least 1 hour.', 'step_time': 60},
            {'step_number': 2, 'text': 'Grill or pan-fry marinated chicken until cooked through. Cut into bite-sized pieces.', 'step_time': 15},
            {'step_number': 3, 'text': 'Melt butter in a pan. Add ginger-garlic paste and cook until fragrant.', 'step_time': 3},
            {'step_number': 4, 'text': 'Add tomato puree, chili powder, and remaining garam masala. Cook for 10 minutes until oil separates.', 'step_time': 10},
            {'step_number': 5, 'text': 'Add cream, fenugreek leaves, and chicken. Simmer for 10 minutes. Garnish with cream and serve.', 'step_time': 10},
        ],
        'prep_time': 70,
        'cook_time': 30,
        'servings': 5,
        'difficulty': 'medium',
        'tags': ['indian', 'curry', 'creamy', 'popular'],
        'categories': ['Dinner', 'Main Course', 'Indian'],
        'cuisine': 'Indian',
        'nutrition': {'calories': 520, 'protein': 38, 'carbs': 12, 'fat': 36, 'fiber': 2, 'sugar': 6},
        'rating_stats': {'average': 4.8, 'count': 312, 'total': 312},
        'views': 5234,
        'cook_count': 267,
        'rarity': 'legendary',
        'is_published': True,
        'is_featured': True,
        'author': user
    },
    {
        'title': 'Greek Moussaka',
        'description': 'Layered casserole with eggplant, spiced meat sauce, and creamy béchamel. A hearty and comforting Greek classic!',
        'images': ['https://images.unsplash.com/photo-1601050690597-df0568f70950?w=800'],
        'ingredients': [
            {'name': 'Eggplants', 'quantity': '3', 'unit': 'large'},
            {'name': 'Ground Lamb', 'quantity': '600', 'unit': 'g'},
            {'name': 'Onions', 'quantity': '2', 'unit': 'large'},
            {'name': 'Tomatoes', 'quantity': '4', 'unit': 'large'},
            {'name': 'Red Wine', 'quantity': '1/2', 'unit': 'cup'},
            {'name': 'Cinnamon', 'quantity': '1', 'unit': 'tsp'},
            {'name': 'Milk', 'quantity': '3', 'unit': 'cups'},
            {'name': 'Flour', 'quantity': '1/2', 'unit': 'cup'},
            {'name': 'Parmesan Cheese', 'quantity': '100', 'unit': 'g'},
        ],
        'steps': [
            {'step_number': 1, 'text': 'Slice eggplants, salt them, and let sit for 30 minutes. Rinse and brush with olive oil. Grill or bake until golden.', 'step_time': 45},
            {'step_number': 2, 'text': 'Brown ground lamb with onions. Add tomatoes, wine, cinnamon, salt, and pepper. Simmer for 30 minutes.', 'step_time': 35},
            {'step_number': 3, 'text': 'Make béchamel: Melt butter, add flour, cook 2 minutes. Gradually whisk in milk. Cook until thick. Add cheese.', 'step_time': 15},
            {'step_number': 4, 'text': 'Layer in baking dish: eggplant, meat sauce, eggplant, meat sauce. Top with béchamel.', 'step_time': 10},
            {'step_number': 5, 'text': 'Bake at 350°F (180°C) for 45 minutes until golden. Let rest 15 minutes before serving.', 'step_time': 60},
        ],
        'prep_time': 40,
        'cook_time': 120,
        'servings': 8,
        'difficulty': 'hard',
        'tags': ['greek', 'casserole', 'comfort-food', 'traditional'],
        'categories': ['Dinner', 'Main Course', 'Greek'],
        'cuisine': 'Greek',
        'nutrition': {'calories': 480, 'protein': 26, 'carbs': 32, 'fat': 28, 'fiber': 8, 'sugar': 12},
        'rating_stats': {'average': 4.7, 'count': 98, 'total': 98},
        'views': 1876,
        'cook_count': 72,
        'rarity': 'epic',
        'is_published': True,
        'is_featured': False,
        'author': user
    },
    {
        'title': 'Vietnamese Pho',
        'description': 'Aromatic beef noodle soup with rice noodles, tender beef slices, and fresh herbs. The ultimate comfort food from Vietnam!',
        'images': ['https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=800'],
        'ingredients': [
            {'name': 'Beef Bones', 'quantity': '1', 'unit': 'kg'},
            {'name': 'Beef Brisket', 'quantity': '500', 'unit': 'g'},
            {'name': 'Rice Noodles', 'quantity': '400', 'unit': 'g'},
            {'name': 'Onions', 'quantity': '2', 'unit': 'large'},
            {'name': 'Ginger', 'quantity': '100', 'unit': 'g'},
            {'name': 'Star Anise', 'quantity': '5', 'unit': 'pieces'},
            {'name': 'Cinnamon Stick', 'quantity': '1', 'unit': 'piece'},
            {'name': 'Fish Sauce', 'quantity': '4', 'unit': 'tbsp'},
            {'name': 'Fresh Herbs', 'quantity': '2', 'unit': 'cups'},
            {'name': 'Bean Sprouts', 'quantity': '200', 'unit': 'g'},
        ],
        'steps': [
            {'step_number': 1, 'text': 'Char onions and ginger over open flame or under broiler until blackened. Rinse.', 'step_time': 10},
            {'step_number': 2, 'text': 'Blanch beef bones in boiling water for 5 minutes. Rinse well to remove impurities.', 'step_time': 10},
            {'step_number': 3, 'text': 'Simmer bones with charred onions, ginger, star anise, and cinnamon for 6-8 hours. Strain broth.', 'step_time': 420},
            {'step_number': 4, 'text': 'Cook brisket in broth until tender, about 2 hours. Remove and slice thinly.', 'step_time': 120},
            {'step_number': 5, 'text': 'Cook rice noodles. Assemble bowls with noodles, beef slices, hot broth, and fresh herbs. Serve with lime and sriracha.', 'step_time': 10},
        ],
        'prep_time': 30,
        'cook_time': 480,
        'servings': 6,
        'difficulty': 'hard',
        'tags': ['vietnamese', 'soup', 'noodles', 'authentic'],
        'categories': ['Lunch', 'Soup', 'Vietnamese'],
        'cuisine': 'Vietnamese',
        'nutrition': {'calories': 420, 'protein': 32, 'carbs': 52, 'fat': 10, 'fiber': 3, 'sugar': 4},
        'rating_stats': {'average': 4.9, 'count': 187, 'total': 187},
        'views': 3456,
        'cook_count': 142,
        'rarity': 'legendary',
        'is_published': True,
        'is_featured': True,
        'author': user
    },
]

created_count = 0
skipped_count = 0

print("🌱 Seeding recipes...")
print("="*60)

for recipe_data in recipes:
    existing = Recipe.objects(title=recipe_data['title']).first()
    if existing:
        print(f"⏭️  Skipped '{recipe_data['title']}' (already exists)")
        skipped_count += 1
    else:
        recipe = Recipe(**recipe_data)
        recipe.save()
        print(f"✅ Created '{recipe.title}'")
        created_count += 1

print("="*60)
print(f"🎉 Seeding complete!")
print(f"   Created: {created_count} recipes")
print(f"   Skipped: {skipped_count} recipes")
print(f"   Total: {Recipe.objects.count()} recipes in database")
print("="*60)
