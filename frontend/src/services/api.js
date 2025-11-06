import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor pentru adăugare JWT token și trailing slash
api.interceptors.request.use(
  (config) => {
    // Add trailing slash if not present (Django requires it for POST/PUT/PATCH)
    if (config.url && !config.url.endsWith('/') && !config.url.includes('?')) {
      config.url += '/';
    }

    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor pentru gestionare erori
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Dacă token-ul a expirat, încearcă refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/auth/refresh`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// ==========================
// Authentication API
// ==========================

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (credentials) => api.post('/auth/login', credentials),
  getCurrentUser: () => api.get('/auth/me'),
};

// ==========================
// User Profiles API
// ==========================

export const profileAPI = {
  getAll: () => api.get('/profiles'),
  getById: (id) => api.get(`/profiles/${id}`),
  getMyProfile: () => api.get('/profiles/me'),
  updateMyProfile: (data) => api.patch('/profiles/me', data),
  getRatings: (id) => api.get(`/profiles/${id}/ratings`),
  getSessions: (id) => api.get(`/profiles/${id}/sesiuni`),
};

// ==========================
// Gyms API
// ==========================

export const gymAPI = {
  getAll: () => api.get('/sali'),
  getById: (id) => api.get(`/sali/${id}`),
};

// ==========================
// Sessions API
// ==========================

export const sessionAPI = {
  getAll: (params) => api.get('/sesiuni', { params }),
  getById: (id) => api.get(`/sesiuni/${id}`),
  getMySessions: () => api.get('/sesiuni/my_sessions'),
  create: (data) => api.post('/sesiuni', data),
  update: (id, data) => api.patch(`/sesiuni/${id}`, data),
  delete: (id) => api.delete(`/sesiuni/${id}`),
  complete: (id) => api.post(`/sesiuni/${id}/complete_session`),
  cancel: (id) => api.post(`/sesiuni/${id}/cancel_session`),
};

// ==========================
// Requests API
// ==========================

export const requestAPI = {
  getAll: () => api.get('/cereri'),
  create: (data) => api.post('/cereri', data),
  update: (id, data) => api.patch(`/cereri/${id}`, data),
  accept: (id) => api.patch(`/cereri/${id}`, { status: 'acceptat' }),
  reject: (id) => api.patch(`/cereri/${id}`, { status: 'refuzat' }),
};

// ==========================
// Ratings API
// ==========================

export const ratingAPI = {
  getAll: () => api.get('/rating'),
  create: (data) => api.post('/rating', data),
};

// ==========================
// Notifications API
// ==========================

export const notificationAPI = {
  getAll: () => api.get('/notifications'),
  getUnreadCount: () => api.get('/notifications/unread_count'),
  markAsRead: (id) => api.post(`/notifications/${id}/mark_as_read`),
  markAllAsRead: () => api.post('/notifications/mark_all_as_read'),
};

// ==========================
// Social API
// ==========================

export const socialAPI = {
  follow: (userId) => api.post('/social/follow', { user_id: userId }),
  unfollow: (userId) => api.post('/social/unfollow', { user_id: userId }),
  getFollowers: () => api.get('/social/followers'),
  getFollowing: () => api.get('/social/following'),
  getUserFollowers: (userId) => api.get(`/social/${userId}/user_followers`),
  getUserFollowing: (userId) => api.get(`/social/${userId}/user_following`),
  getActivityFeed: () => api.get('/social/activity_feed'),
  getSuggestions: () => api.get('/social/suggestions'),
  isFollowing: (userId) => api.get(`/social/${userId}/is_following`),
};

export default api;
