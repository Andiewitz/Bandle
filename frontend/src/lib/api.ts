import axios from 'axios';

// Create an Axios instance configured for our dual-database backend
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  // Essential for sending HttpOnly secure cookies cross-origin
  withCredentials: true, 
});

// We store the CSRF token in memory, not localStorage, to prevent XSS exfiltration
let csrfToken: string | null = null;

export const setCsrfToken = (token: string | null) => {
  csrfToken = token;
};

// Request interceptor to automatically attach the CSRF token to mutating requests
api.interceptors.request.use((config) => {
  if (csrfToken && ['post', 'put', 'delete', 'patch'].includes(config.method || '')) {
    config.headers['X-CSRF-Token'] = csrfToken;
  }
  return config;
});

export default api;
