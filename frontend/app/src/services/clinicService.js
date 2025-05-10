import api from './api';

const clinicService = {
  getProfile: () => {
    return api.get('auth/clinic/profile');
  },

  updateProfile: (profileData) => { // name, phone
    return api.put('auth/clinic/profile', profileData);
  },
};

export default clinicService; 