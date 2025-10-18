import React from 'react';
import Header from '../components/Header';
import { useNavigate } from 'react-router-dom';

type VulcanoPageProps = {
  children: React.ReactNode;
};

const VulcanoPage: React.FC<VulcanoPageProps> = ({ children }) => {
  const navigate = useNavigate();

  const goHome = () => {
    navigate('/');
  };

  return (
    <>
      <Header isLoggedIn={true} onLogout={goHome} />
      <div className="vulcano-page">{children}</div>
    </>
  );
};

export default VulcanoPage;