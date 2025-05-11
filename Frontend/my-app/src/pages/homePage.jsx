import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-4xl font-bold mb-8">Welcome to Account Manager</h1>
      <div className="space-x-4">
        <Link to="/cards">
          <button className="px-6 py-3 bg-blue-600 text-white rounded-2xl shadow hover:bg-blue-700">
            Manage Cards
          </button>
        </Link>
        <Link to="/passwords">
          <button className="px-6 py-3 bg-green-600 text-white rounded-2xl shadow hover:bg-green-700">
            Manage Passwords
          </button>
        </Link>
      </div>
    </div>
  );
};

export default HomePage;