import axios from 'axios';

// Ensure this matches your FastAPI backend URL or environment variable
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

// Intercept requests to attach JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Intercept responses to redirect to login on 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    } else if (error.response && error.response.status >= 400) {
      const data = error.response.data;
      const reqId = data?.request_id || error.response.headers?.['x-request-id'] || 'unknown';
      const msg = data?.detail || data?.error || 'Request Failed';
      alert(`${msg}
Reference: ${reqId}`);
    } else {
      alert(`Network Error
Reference: unknown`);
    }
    return Promise.reject(error);
  }
);
