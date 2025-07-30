import React from 'react';
import { AuthProvider } from './contexts/AuthContext';
import { ClientAuthProvider } from './client/contexts/ClientAuthContext';
import AppRoutes from './routes';

function App() {
  return (
    <ClientAuthProvider>
      <AppRoutes />
    </ClientAuthProvider>
  );
}

export default App;
