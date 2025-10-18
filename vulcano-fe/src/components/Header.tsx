import React from 'react';
import QuestionMarkIcon from '../assets/question-mark.png';

interface HeaderProps {
  isLoggedIn?: boolean;
  onLogout?: () => void;
}

const Header: React.FC<HeaderProps> = ({ isLoggedIn = false, onLogout }) => (
  <div className="app-header">
    <div className="app-header-left">
      <img src={QuestionMarkIcon} alt="Logo" className="app-header-logo" />
    </div>
    <div className="app-header-right">
      {isLoggedIn && (
        <span className="app-header-logout" onClick={onLogout}>
          Logout
        </span>
      )}
    </div>
  </div>
);

export default Header;