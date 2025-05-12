import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './homePage.css';

const HomePage = () => {
  const navigate = useNavigate();

  const API_BASE = process.env.REACT_APP_API_BASE_URL;

  const handleLogout = async () => {
    try {
      const response = await fetch(`${API_BASE}/auth/logout`, {
        method: 'POST',
        credentials: 'include',
      });

      if (response.ok) {
        navigate('/'); // Redirect to login
      } else {
        console.error('Logout failed');
      }
    } catch (error) {
      console.error('Error during logout:', error);
    }
  };
  

  return (
    <div className="home-container">
      <div className="home-card">
        <h1>Welcome to Account Manager</h1>
        <p>Securely manage your cards and passwords in one place.</p>
        <Link to="/cards">
          <button className="home-button cards">Manage Cards</button>
        </Link>
        <Link to="/passwords">
          <button className="home-button passwords">Manage Passwords</button>
        </Link>
        <button onClick={handleLogout} className="home-button logout">
          Logout
        </button>
      </div>
    </div>
  );
};

export default HomePage;