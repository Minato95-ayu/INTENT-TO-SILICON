import axios from 'axios';

// Ensure this matches your FastAPI backend URL or environment variable
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});
