import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // URL base da sua API backend
});

// Adiciona um interceptor de requisição
api.interceptors.request.use(
  (config) => {
    // Verificar se já existe um header Authorization na requisição
    if (config.headers.Authorization) {
      console.log(`Axios Interceptor: Header Authorization já definido: ${config.headers.Authorization}`);
      return config;
    }
    
    // Primeiro, tentar o token de cliente
    const clientToken = localStorage.getItem('client_token');
    if (clientToken) {
      config.headers.Authorization = `Bearer ${clientToken}`;
      console.log(`Axios Interceptor: Token de cliente ('client_token') usado: ${clientToken}`);
      return config;
    }
    
    // Se não houver token de cliente, usar o token de clínica
    const clinicToken = localStorage.getItem('viteToken');
    if (clinicToken) {
      config.headers.Authorization = `Bearer ${clinicToken}`;
      console.log(`Axios Interceptor: Token de clínica ('viteToken') usado: ${clinicToken}`);
    } else {
      console.log(`Axios Interceptor: Nenhum token encontrado no localStorage.`);
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