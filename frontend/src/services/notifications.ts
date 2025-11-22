import apiClient from './api';

export interface Notification {
  id: string;
  type: 'comment' | 'comment_like' | 'badge_earned' | 'level_up' | 'recipe_cooked' | 'new_follower' | 'recipe_liked' | 'mention';
  title: string;
  message: string;
  related_object?: string;
  is_read: boolean;
  created_at: string;
  sender?: {
    id: string;
    username: string;
    avatar_url?: string;
  };
}

export interface NotificationsResponse {
  count: number;
  page: number;
  limit: number;
  total_pages: number;
  results: Notification[];
}

export const notificationService = {
  async getNotifications(page: number = 1, unread_only: boolean = false): Promise<NotificationsResponse> {
    const response = await apiClient.get<NotificationsResponse>('/api/notifications/', {
      params: { page, limit: 20, unread_only }
    });
    return response.data;
  },

  async getUnreadCount(): Promise<{ unread_count: number }> {
    const response = await apiClient.get<{ unread_count: number }>('/api/notifications/unread-count/');
    return response.data;
  },

  async markAsRead(notificationId: string): Promise<void> {
    await apiClient.post(`/api/notifications/${notificationId}/read/`);
  },

  async markAllAsRead(): Promise<void> {
    await apiClient.post('/api/notifications/mark-all-read/');
  },

  async deleteNotification(notificationId: string): Promise<void> {
    await apiClient.delete(`/api/notifications/${notificationId}/`);
  },
};
