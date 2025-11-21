// API Types matching backend models

export interface User {
  id: string;
  username: string;
  email: string;
  avatar_url?: string;
  bio?: string;
  xp: number;
  level: number;
  badges: string[];
  followers_count: number;
  following_count: number;
  preferences: {
    cuisines: string[];
    dietary_restrictions: string[];
    favorite_tags: string[];
  };
  created_at: string;
}

export interface Ingredient {
  name: string;
  quantity: string;
  unit: string;
  optional?: boolean;
}

export interface RecipeStep {
  step_number: number;
  text: string;
  image?: string;
  step_time?: number;
}

export interface NutritionInfo {
  calories?: number;
  protein?: number;
  carbs?: number;
  fat?: number;
  fiber?: number;
  sugar?: number;
}

export interface RatingStats {
  average: number;
  count: number;
}

export interface Recipe {
  id: string;
  title: string;
  slug: string;
  description: string;
  images: string[];
  ingredients: Ingredient[];
  steps: RecipeStep[];
  prep_time: number;
  cook_time: number;
  total_time: number;
  servings: number;
  difficulty: 'easy' | 'medium' | 'hard';
  tags: string[];
  categories: string[];
  cuisine: string;
  nutrition_info?: NutritionInfo;
  rating_stats: RatingStats;
  views: number;
  cook_count: number;
  rarity: 'common' | 'uncommon' | 'rare' | 'legendary';
  is_published: boolean;
  is_featured: boolean;
  author: {
    id: string;
    username: string;
    avatar_url?: string;
    level: number;
  };
  created_at: string;
  updated_at: string;
}

export interface RecipeListItem {
  id: string;
  title: string;
  slug: string;
  description: string;
  images: string[];
  prep_time: number;
  cook_time: number;
  total_time: number;
  servings: number;
  difficulty: 'easy' | 'medium' | 'hard';
  tags: string[];
  cuisine: string;
  rating_stats: RatingStats;
  views: number;
  cook_count: number;
  rarity: 'common' | 'uncommon' | 'rare' | 'legendary';
  author: {
    id: string;
    username: string;
    avatar_url?: string;
    level: number;
  };
  created_at: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  user: User;
  access: string;
  refresh: string;
}

export interface CreateRecipeRequest {
  title: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard';
  prep_time: number;
  cook_time: number;
  servings: number;
  tags: string[];
  cuisine: string;
  ingredients: Ingredient[];
  steps: RecipeStep[];
  images?: string[];
  nutrition_info?: NutritionInfo;
}

export interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  tier: 'bronze' | 'silver' | 'gold' | 'diamond';
  xp_reward: number;
}

export interface RecipeFilters {
  q?: string;
  tags?: string[];
  difficulty?: 'easy' | 'medium' | 'hard';
  cuisine?: string;
  time_max?: number;
  sort?: string;
  page?: number;
  page_size?: number;
}
