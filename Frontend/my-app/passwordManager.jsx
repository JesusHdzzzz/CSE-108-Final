import React, { useEffect, useState } from 'react';
import axios from 'axios';

const passwordManager = () => {
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
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Your Saved Passwords</h2>
      {passwords.length === 0 ? (
        <p>No passwords found.</p>
      ) : (
        <ul className="space-y-2">
          {passwords.map((entry, idx) => (
            <li key={idx} className="p-4 border rounded-xl bg-white shadow">
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

export default passwordManager;