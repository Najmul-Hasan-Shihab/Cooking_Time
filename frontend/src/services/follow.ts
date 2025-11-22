import apiClient from './api';

export interface FollowUser {
  id: string;
  username: string;
  level: number;
  xp: number;
  followers_count: number;
  is_following: boolean;
}

export interface FollowResponse {
  count: number;
  page: number;
  limit: number;
  total_pages: number;
  results: FollowUser[];
}

export interface FeedRecipe {
  id: string;
  slug: string;
  title: string;
  description: string;
  author: {
    id: string;
    username: string;
    level: number;
  };
  images: string[];
  difficulty: string;
  total_time: number;
  rating_stats: {
    average: number;
    count: number;
  };
  created_at: string;
}

export interface FeedResponse {
  count: number;
  page: number;
  limit: number;
  total_pages: number;
  results: FeedRecipe[];
}

export const followService = {
  async toggleFollow(userId: string): Promise<{ action: string; is_following: boolean; followers_count: number; following_count: number }> {
    const response = await apiClient.post(`/api/users/${userId}/follow/`);
    return response.data;
  },

  async getFollowers(userId: string, page: number = 1): Promise<FollowResponse> {
    const response = await apiClient.get<FollowResponse>(`/api/users/${userId}/followers/`, {
      params: { page, limit: 20 }
    });
    return response.data;
  },

  async getFollowing(userId: string, page: number = 1): Promise<FollowResponse> {
    const response = await apiClient.get<FollowResponse>(`/api/users/${userId}/following/`, {
      params: { page, limit: 20 }
    });
    return response.data;
  },

  async getActivityFeed(page: number = 1): Promise<FeedResponse> {
    const response = await apiClient.get<FeedResponse>('/api/users/feed/', {
      params: { page, limit: 20 }
    });
    return response.data;
  },
};
