import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './passwordManager.css';

const PasswordManager = () => {
  const [passwords, setPasswords] = useState([]);

  useEffect(() => {
    fetchPasswords();
  }, []);

  const fetchPasswords = async () => {
    try {
      const response = await axios.get('/passwords/all');
      setPasswords(response.data.passwords);
    } catch (err) {
      console.error('Error fetching passwords:', err);
    }
  };

  return (
    <div className="password-manager-container">
      <h2 className="password-manager-title">Your Saved Passwords</h2>
      {passwords.length === 0 ? (
        <p>No passwords found.</p>
      ) : (
        <ul className="password-list">
          {passwords.map((entry, idx) => (
            <li key={idx} className="password-item">
              <div><strong>Website:</strong> {entry.website_name}</div>
              <div><strong>Password:</strong> {entry.password}</div>
              <div><strong>Group:</strong> {entry.group_name}</div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default PasswordManager;