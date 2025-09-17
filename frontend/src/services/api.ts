import axios from 'axios';
import { User, LoginData, FeedbackData, WaitingMatch } from '../types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth API
export const authAPI = {
  login: async (data: LoginData) => {
    const response = await api.post('/login/login', data);
    return response.data;
  },
  
  register: async (data: LoginData) => {
    const response = await api.post('/login/register', data);
    return response.data;
  },
  
  verifyToken: async (token: string) => {
    const response = await api.post('/login/protected', { token });
    return response.data;
  }
};

// OpenAPI Schema API
export const openApiAPI = {
  getSchema: async () => {
    const response = await api.get('/openapi.json');
    return response.data;
  },

  makeRequest: async (method: string, path: string, params?: Record<string, unknown>, data?: Record<string, unknown>) => {
    try {
      const response = await api.request({
        method,
        url: path,
        params,
        data,
      });
      return response.data;
    } catch (error: unknown) {
      // @ts-expect-error: error is of type unknown
      return error.response.data;
    }
  }
};

// Profile API
export const profileAPI = {
  addPerson: async (userData: User, photo?: File) => {
    const formData = new FormData();
    
    // Add all user data as form fields
    Object.entries(userData).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        if (Array.isArray(value)) {
          formData.append(key, JSON.stringify(value));
        } else {
          formData.append(key, value.toString());
        }
      }
    });
    
    if (photo) {
      formData.append('file', photo);
    }
    
    const response = await api.post('/add_person/add_person', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }
};

// Matches API
export const matchesAPI = {
  getWaitingMatches: async (actorId: string): Promise<{ waiting: WaitingMatch[] }> => {
    const response = await api.get(`/waiting_matches/${actorId}`);
    return response.data;
  },
  
  sendFeedback: async (feedback: FeedbackData) => {
    const response = await api.post('/likes/feedback', feedback);
    return response.data;
  }
};