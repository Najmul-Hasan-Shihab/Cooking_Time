# Code Style Guide

## General Principles

- Write clean, readable, and maintainable code
- Follow DRY (Don't Repeat Yourself) principle
- Use meaningful variable and function names
- Comment complex logic, not obvious code
- Keep functions small and focused on a single responsibility

## Python (Backend)

### Style Guide
Follow [PEP 8](https://peps.python.org/pep-0008/) guidelines.

### Formatting
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use blank lines to separate logical sections

### Naming Conventions
```python
# Classes: PascalCase
class RecipeModel:
    pass

# Functions and variables: snake_case
def calculate_xp_for_action(action_type):
    user_xp = 0
    return user_xp

# Constants: UPPER_SNAKE_CASE
MAX_UPLOAD_SIZE = 5242880  # 5MB

# Private methods/attributes: prefix with underscore
def _internal_helper():
    pass
```

### Imports
```python
# Standard library imports first
import os
import sys

# Third-party imports
from django.db import models
from rest_framework import serializers

# Local application imports
from .models import Recipe
from .utils import calculate_difficulty
```

### Django Specific
- Use Django ORM methods over raw queries when possible
- Use serializers for data validation
- Keep views thin, business logic in services/managers
- Use Django's built-in validators

### Example
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Recipe CRUD operations.
    Provides list, create, retrieve, update, and delete actions.
    """
    
    @action(detail=True, methods=['post'])
    def mark_cooked(self, request, pk=None):
        """Mark a recipe as cooked and award XP to the user."""
        recipe = self.get_object()
        user = request.user
        
        # Award XP and create action record
        xp_awarded = award_xp(user, 'cook', recipe)
        
        return Response({
            'message': 'Recipe marked as cooked',
            'xp_awarded': xp_awarded
        }, status=status.HTTP_200_OK)
```

## JavaScript/TypeScript (Frontend)

### Style Guide
Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript).

### Formatting
- Use 2 spaces for indentation
- Use single quotes for strings
- Always use semicolons
- Maximum line length: 100 characters

### Naming Conventions
```typescript
// Components: PascalCase
const RecipeCard = () => { ... }

// Functions and variables: camelCase
const calculateLevel = (xp: number) => { ... }

// Constants: UPPER_SNAKE_CASE
const MAX_RECIPES_PER_PAGE = 20;

// Interfaces/Types: PascalCase with 'I' prefix for interfaces (optional)
interface Recipe {
  id: string;
  title: string;
}

type RecipeDifficulty = 'easy' | 'medium' | 'hard';
```

### React Specific
- Use functional components with hooks
- One component per file
- Use TypeScript for type safety
- Props interface should be named `ComponentNameProps`
- Use descriptive prop names

### Example
```typescript
import { useState, useEffect } from 'react';
import { Recipe } from '../types';
import { fetchRecipe } from '../api/recipes';

interface RecipeCardProps {
  recipeId: string;
  onCook?: (recipeId: string) => void;
  showActions?: boolean;
}

const RecipeCard: React.FC<RecipeCardProps> = ({ 
  recipeId, 
  onCook, 
  showActions = true 
}) => {
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadRecipe = async () => {
      try {
        const data = await fetchRecipe(recipeId);
        setRecipe(data);
      } catch (error) {
        console.error('Failed to load recipe:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadRecipe();
  }, [recipeId]);

  if (isLoading) return <LoadingSkeleton />;
  if (!recipe) return <ErrorMessage />;

  return (
    <div className="recipe-card">
      <h3>{recipe.title}</h3>
      {showActions && (
        <button onClick={() => onCook?.(recipeId)}>
          Mark as Cooked
        </button>
      )}
    </div>
  );
};

export default RecipeCard;
```

## CSS/TailwindCSS

### Guidelines
- Use TailwindCSS utility classes for styling
- Create custom components for repeated patterns
- Use CSS modules for component-specific styles
- Follow mobile-first responsive design

### Example
```tsx
// Good: Using Tailwind utilities
<div className="flex flex-col gap-4 p-6 bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow">
  <h2 className="text-2xl font-bold text-gray-800">{title}</h2>
  <p className="text-gray-600">{description}</p>
</div>

// For complex reusable styles, extract to component
const Card = ({ children, variant = 'default' }) => {
  const variants = {
    default: 'bg-white',
    rare: 'bg-gradient-to-br from-purple-400 to-pink-400',
    epic: 'bg-gradient-to-br from-yellow-400 to-orange-500'
  };
  
  return (
    <div className={`rounded-lg p-6 shadow-lg ${variants[variant]}`}>
      {children}
    </div>
  );
};
```

## Git Commit Messages

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(recipes): add mark as cooked functionality

Implement the ability for users to mark recipes as cooked
and award XP for the action.

Closes #42

---

fix(auth): resolve JWT token refresh issue

The token refresh endpoint was returning 401 errors when
valid refresh tokens were provided.

---

docs: update API documentation for recipe endpoints
```

## Testing

### Python Tests
```python
from django.test import TestCase
from .models import Recipe


class RecipeModelTest(TestCase):
    """Test suite for Recipe model."""
    
    def setUp(self):
        """Set up test data."""
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            description='A test recipe'
        )
    
    def test_recipe_creation(self):
        """Test that recipe is created correctly."""
        self.assertEqual(self.recipe.title, 'Test Recipe')
        self.assertIsNotNone(self.recipe.created_at)
```

### React Tests
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import RecipeCard from './RecipeCard';

describe('RecipeCard', () => {
  const mockRecipe = {
    id: '1',
    title: 'Test Recipe',
    description: 'Test description'
  };

  it('renders recipe title', () => {
    render(<RecipeCard recipe={mockRecipe} />);
    expect(screen.getByText('Test Recipe')).toBeInTheDocument();
  });

  it('calls onCook when button is clicked', () => {
    const handleCook = jest.fn();
    render(<RecipeCard recipe={mockRecipe} onCook={handleCook} />);
    
    fireEvent.click(screen.getByText('Mark as Cooked'));
    expect(handleCook).toHaveBeenCalledWith('1');
  });
});
```

## Code Review Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New code has appropriate test coverage
- [ ] No console.log or debugging statements
- [ ] Error handling is implemented
- [ ] Documentation is updated
- [ ] Commit messages follow convention
- [ ] No sensitive data in code
