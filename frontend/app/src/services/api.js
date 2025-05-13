import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // URL base da sua API backend
});

// Adiciona um interceptor de requisição
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('viteToken');
    console.log(`Axios Interceptor: Token lido ('viteToken'): ${token}`);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log(`Axios Interceptor: Header Authorization configurado: ${config.headers.Authorization}`);
    } else {
      console.log(`Axios Interceptor: Token ('viteToken') não encontrado no localStorage.`);
    }
    return config;
  },
  (error) => {
    // Faça algo com o erro da requisição
    console.error('Axios Interceptor: Erro na configuração da requisição:', error); // Log para debug
    return Promise.reject(error);
  }
);

// Você pode adicionar interceptors aqui se precisar (ex: para refresh token)
// api.interceptors.response.use(...);

export default api; 