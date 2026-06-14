import axios from 'axios';

// Ensure this matches your FastAPI backend URL
export const api = axios.create({
  baseURL: 'http://localhost:8000',
});
