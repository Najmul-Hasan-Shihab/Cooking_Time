import { useQuery } from '@tanstack/react-query';
import { recipeService } from '../services/recipes';
import { RecipeFilters } from '../types';

export const useRecipes = (filters?: RecipeFilters) => {
  return useQuery({
    queryKey: ['recipes', filters],
    queryFn: () => recipeService.getRecipes(filters),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
};

export const useRecipe = (slug: string) => {
  return useQuery({
    queryKey: ['recipe', slug],
    queryFn: () => recipeService.getRecipeBySlug(slug),
    enabled: !!slug,
  });
};
