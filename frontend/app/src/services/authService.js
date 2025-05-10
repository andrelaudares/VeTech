import api from './api';

const authService = {
  login: (email, password) => {
    return api.post('/auth/login', { email, password });
  },

  register: (userData) => { // name, email, phone, password, subscription_tier
    return api.post('/auth/register', userData);
  },

  logout: () => {
    // A API de logout do backend apenas retorna uma mensagem e não invalida o token no servidor.
    // A invalidação principal ocorre no cliente (removendo o token).
    // Mas podemos chamar o endpoint mesmo assim, se desejado, para seguir o contrato da API.
    return api.post('/auth/logout');
    // Se não houver necessidade de chamar o backend:
    // return Promise.resolve({ message: "Logout no cliente bem-sucedido." });
  },

  // Futuramente, se precisar obter o perfil via authService:
  // getProfile: () => {
  //   return api.get('/clinic/profile'); // Supondo que esta rota esteja sob /auth ou seja pública de outra forma
  // }
};

export default authService; 