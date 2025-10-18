import React from 'react';
import Header from '../components/Header';
import { useAuth } from "../context/AuthContext";
import { useNavigate } from 'react-router-dom';

type VulcanoPageProps = {
  children: React.ReactNode;
};

const VulcanoPage: React.FC<VulcanoPageProps> = ({ children }) => {
  const navigate = useNavigate();
  const { isAuthenticated, logout} = useAuth();

  const goHome = () => {
    logout();
    navigate('/');
  };

  return (
    <>
      <Header isLoggedIn={isAuthenticated} onLogout={goHome} />
      <div className="vulcano-page">{children}</div>
    </>
  );
};

export default VulcanoPage;