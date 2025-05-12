import React, { useState } from 'react';
import './signUpPage.css'; // Your styling here

const SignUpPage = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const handleSignUp = async (e) => {
    e.preventDefault();

    const API_BASE = process.env.REACT_APP_API_BASE_URL;
    if (password !== confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email, password })
      });

      const data = await response.json();

      if (response.ok) {
        setSuccessMsg(data.message);
        setErrorMsg('');
        console.log("User registered with user_id:", data.user_id);
        // Redirect to login page? Clear form? Store user?
      } else {
        alert(data.error || 'Signup failed');
      }
    } catch (err) {
      console.error('Error:', err);
      alert('Server error');
    }
  };

  return (
    <div className="signup-container">
      <form className="signup-form" onSubmit={handleSignUp}>
        <h2>Sign Up</h2>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />
        <button type="submit">Sign Up</button>
        <p className="login-link">
          Already have an account? <a href="/">Login</a>
        </p>
      </form>
    </div>
  );
};

export default SignUpPage;