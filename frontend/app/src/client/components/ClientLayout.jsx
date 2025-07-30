import { Outlet } from 'react-router-dom';
import ClientNavbar from '../components/ClientNavbar';

const ClientLayout = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <ClientNavbar />
      <main>
        <Outlet />
      </main>
    </div>
  );
};

export default ClientLayout;