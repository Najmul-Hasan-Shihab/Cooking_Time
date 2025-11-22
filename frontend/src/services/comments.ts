import apiClient from './api';

export interface Comment {
  id: string;
  recipe: string;
  author: {
    id: string;
    username: string;
    level: number;
  };
  content: string;
  likes_count: number;
  is_liked: boolean;
  created_at: string;
  updated_at: string;
}

export interface CommentsResponse {
  comments: Comment[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    total_pages: number;
    has_next: boolean;
    has_prev: boolean;
  };
}

export interface CreateCommentRequest {
  content: string;
}

export const commentService = {
  async getComments(recipeSlug: string, page: number = 1): Promise<CommentsResponse> {
    const response = await apiClient.get<CommentsResponse>(`/api/recipes/${recipeSlug}/comments/`, {
      params: { page }
    });
    return response.data;
  },

  async createComment(recipeSlug: string, content: string): Promise<{ comment: Comment; xp_awarded: number }> {
    const response = await apiClient.post(`/api/recipes/${recipeSlug}/comments/`, { content });
    return response.data;
  },

  async updateComment(recipeSlug: string, commentId: string, content: string): Promise<Comment> {
    const response = await apiClient.put(`/api/recipes/${recipeSlug}/comments/${commentId}/`, { content });
    return response.data;
  },

  async deleteComment(recipeSlug: string, commentId: string): Promise<void> {
    await apiClient.delete(`/api/recipes/${recipeSlug}/comments/${commentId}/`);
  },

  async toggleLike(recipeSlug: string, commentId: string): Promise<{ is_liked: boolean; likes_count: number }> {
    const response = await apiClient.post(`/api/recipes/${recipeSlug}/comments/${commentId}/like/`);
    return response.data;
  },
};
