import apiClient from './api';

export interface LeaderboardUser {
  rank: number;
  user: {
    id: string;
    username: string;
    level: number;
    xp: number;
  };
  stats: {
    recipes_created: number;
    recipes_cooked: number;
  };
}

export interface LeaderboardResponse {
  count: number;
  page: number;
  limit: number;
  total_pages: number;
  results: LeaderboardUser[];
}

export const leaderboardService = {
  async getByXP(timeframe: string = 'all', page: number = 1): Promise<LeaderboardResponse> {
    const response = await apiClient.get<LeaderboardResponse>('/api/leaderboard/xp/', {
      params: { timeframe, page, limit: 50 }
    });
    return response.data;
  },

  async getByRecipes(page: number = 1): Promise<LeaderboardResponse> {
    const response = await apiClient.get<LeaderboardResponse>('/api/leaderboard/recipes/', {
      params: { page, limit: 50 }
    });
    return response.data;
  },

  async getByCooked(page: number = 1): Promise<LeaderboardResponse> {
    const response = await apiClient.get<LeaderboardResponse>('/api/leaderboard/cooked/', {
      params: { page, limit: 50 }
    });
    return response.data;
  },
};
