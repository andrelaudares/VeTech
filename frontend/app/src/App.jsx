import React from 'react';
// import reactLogo from './assets/react.svg' // Comentado ou removido se não usado
// import viteLogo from '/vite.svg' // Comentado ou removido se não usado
// import './App.css'; // Se os estilos do App.css não forem mais necessários globalmente
import AppRoutes from './routes'; // Importar AppRoutes

function App() {
  // const [count, setCount] = useState(0) // Código de exemplo do Vite, pode ser removido

  return (
    <AppRoutes /> // Renderizar o componente de rotas
  );
}

export default App;
