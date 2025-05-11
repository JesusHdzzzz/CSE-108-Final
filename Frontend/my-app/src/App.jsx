import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LoginPage from './pages/loginPage';
import SignUpPage from './pages/signUpPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/signup" element={<SignUpPage />} />
      <Route path="/home" element={<homePage />} />
      <Route path="/cards" element={<cardManager />} />
      <Route path="/passwords" element={<passwordManager />} />
    </Routes>
  );
}

export default App;
