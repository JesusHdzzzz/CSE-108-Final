import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LoginPage from './pages/loginPage';
import SignUpPage from './pages/signUpPage';
import HomePage from './pages/homePage';
import CardManager from './pages/cardManager';
import PasswordManager from './pages/passwordManager';

function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/signup" element={<SignUpPage />} />
      <Route path="/home" element={<HomePage />} />
      <Route path="/cards" element={<CardManager />} />
      <Route path="/passwords" element={<PasswordManager />} />
    </Routes>
  );
}

export default App;
