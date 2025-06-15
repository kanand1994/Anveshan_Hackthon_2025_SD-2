// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL
});

// Add token to requests
api.interceptors.request.use(config => {
  const user = JSON.parse(localStorage.getItem('user'));
  if (user && user.token) {
    config.headers.Authorization = `Bearer ${user.token}`;
    console.log("Adding token to request:", user.token.substring(0, 20) + "...");
  }
  return config;
});

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      console.error("Authentication error, logging out");
      localStorage.removeItem('user');
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

// Export functions
export const getTimeline = () => api.get('/timeline/timeline');
export const getEvents = () => api.get('/events/');
export const createEvent = (event) => api.post('/events/', event);
export const getEventById = (id) => api.get(`/events/${id}`);
export const updateEvent = (id, event) => api.put(`/events/${id}`, event);
export const deleteEvent = (id) => api.delete(`/events/${id}`);
export const getEventsSummary = () => api.get('/events/summary');
export const restoreEvent = (id) => api.post(`/events/${id}/restore`);