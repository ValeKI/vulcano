import React from 'react';
import LoginBox from '../components/LoginBox';
import VulcanoPage from './VulcanoPage';

const Home: React.FC = () => {
  return (
    <VulcanoPage>
    <div className="login">
      <LoginBox />
    </div>
    </VulcanoPage>
  );
};

export default Home;