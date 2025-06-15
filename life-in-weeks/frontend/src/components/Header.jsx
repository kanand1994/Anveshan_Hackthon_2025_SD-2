import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';

export default function Header() {
  const { currentUser, logout } = useAuth();
  const location = useLocation();

  return (
    <header className="app-header">
      <div className="header-left">
        <h1>Life-In-Weeks Timeline</h1>
        {currentUser && (
          <nav>
            <Link to="/" className={location.pathname === '/' ? 'active' : ''}>
              Timeline
            </Link>
            <Link to="/events" className={location.pathname === '/events' ? 'active' : ''}>
              Event Summary
            </Link>
          </nav>
        )}
      </div>
      
      {currentUser && (
        <div className="user-info">
          <span>{currentUser.email}</span>
          <button onClick={logout}>Logout</button>
        </div>
      )}
    </header>
  );
}