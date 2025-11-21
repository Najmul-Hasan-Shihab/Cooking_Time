import apiClient from './api';
import {
  Recipe,
  RecipeListItem,
  PaginatedResponse,
  CreateRecipeRequest,
  RecipeFilters,
} from '../types';

export const recipeService = {
  async getRecipes(filters?: RecipeFilters): Promise<PaginatedResponse<RecipeListItem>> {
    const params = new URLSearchParams();
    
    if (filters?.q) params.append('q', filters.q);
    if (filters?.tags) filters.tags.forEach(tag => params.append('tags', tag));
    if (filters?.difficulty) params.append('difficulty', filters.difficulty);
    if (filters?.cuisine) params.append('cuisine', filters.cuisine);
    if (filters?.time_max) params.append('time_max', filters.time_max.toString());
    if (filters?.sort) params.append('sort', filters.sort);
    if (filters?.page) params.append('page', filters.page.toString());
    if (filters?.page_size) params.append('page_size', filters.page_size.toString());

    const response = await apiClient.get<PaginatedResponse<RecipeListItem>>(
      `/api/recipes/?${params.toString()}`
    );
    return response.data;
  },

  async getRecipeBySlug(slug: string): Promise<Recipe> {
    const response = await apiClient.get<Recipe>(`/api/recipes/${slug}/`);
    return response.data;
  },

  async createRecipe(data: CreateRecipeRequest): Promise<Recipe> {
    const response = await apiClient.post<Recipe>('/api/recipes/', data);
    return response.data;
  },

  async updateRecipe(slug: string, data: Partial<CreateRecipeRequest>): Promise<Recipe> {
    const response = await apiClient.put<Recipe>(`/api/recipes/${slug}/`, data);
    return response.data;
  },

  async deleteRecipe(slug: string): Promise<void> {
    await apiClient.delete(`/api/recipes/${slug}/`);
  },

  async markAsCooked(slug: string): Promise<{ message: string; xp_awarded: number; user: { xp: number; level: number } }> {
    const response = await apiClient.post(`/api/recipes/${slug}/mark_cooked/`);
    return response.data;
  },
};
