/**
 * API Service Layer
 * Handles all HTTP requests to the backend API
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 seconds for AI generation
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

/**
 * Generate a LinkedIn post from a given topic
 * @param {string} topic - The topic to generate post about
 * @returns {Promise} API response with generated post
 */
export const generateLinkedInPost = (topic) => {
  return apiClient.post('/api/v1/generate-post', { topic });
};

/**
 * Health check endpoint
 * @returns {Promise} API health status
 */
export const healthCheck = () => {
  return apiClient.get('/api/v1/health');
};
