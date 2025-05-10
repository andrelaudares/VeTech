import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // URL base da sua API backend
});

// Você pode adicionar interceptors aqui se precisar (ex: para refresh token)
// api.interceptors.response.use(...);

export default api; 