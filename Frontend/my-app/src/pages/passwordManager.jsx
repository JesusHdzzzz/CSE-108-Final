import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './passwordManager.css';

const PasswordManager = () => {
  const [passwords, setPasswords] = useState([]);
  const [newPass, setNewPass] = useState({ website_name: '', web_pass: '' });
  const [updatePass, setUpdatePass] = useState({
    website_name: '',
    old_pass: '',
    new_pass: '',
    confirm_pass: ''
  });
  const [deleteWebsite, setDeleteWebsite] = useState('');
  const [selectedWebsite, setSelectedWebsite] = useState('');
  const [revealedPassword, setRevealedPassword] = useState('');
  //const [websiteUrlPrompt, setWebsiteUrlPrompt] = useState('');

  useEffect(() => {
    fetchPasswords();
  }, []);

  const API_BASE = process.env.REACT_APP_API_BASE_URL;

  const handleRevealPassword = async (e) => {
    e.preventDefault();

    const confirmed = window.confirm(`Reveal password for ${selectedWebsite}?`);
    if (!confirmed) return;

    try {
      const response = await axios.post(`${API_BASE}/passwords/website/view`, {
        website_name: selectedWebsite
      }, {
        withCredentials: true
      });
      setRevealedPassword(response.data["Website password"]);
    } catch (err) {
      console.error("Error fetching password:", err.response?.data || err.message);
      alert("Could not fetch password.");
    }
  };  

  const fetchPasswords = async () => {
    try {
      const response = await axios.get(`${API_BASE}/passwords/all`, {
        withCredentials: true
      });
      const data = response.data;

      if (data.Passwords) {
        setPasswords(data.Passwords);
      } else {
        console.warn("No passwords found in response:", data);
        setPasswords([]);
      }
    } catch (err) {
      console.error('Error fetching passwords:', err);
    }
  };

  const handleAddPassword = async (e) => {
    e.preventDefault();

    try {
      // Step 1: Try to save password
      await axios.post(`${API_BASE}/passwords/website`, newPass, {
        withCredentials: true
      });
      alert("Password added!");
      setNewPass({ website_name: '', web_pass: '' });
      fetchPasswords();
    } catch (err) {
      const errorMsg = err.response?.data?.error;

      if (errorMsg?.includes('website does not exist')) {
        const url = window.prompt(
          `Website "${newPass.website_name}" does not exist. Enter URL to create it:`
        );

        if (!url) return;

        try {
          // Step 2: Create the website first
          await axios.post(`${API_BASE}/passwords/websites`, {
            website_name: newPass.website_name,
            website_url: url,
          }, {
            withCredentials: true
          });

          // Step 3: Retry adding password
          await axios.post(`${API_BASE}/passwords/website`, newPass, {
            withCredentials: true
          });
          alert("Password added after creating website.");
          setNewPass({ website_name: '', web_pass: '' });
          fetchPasswords();
        } catch (createErr) {
          console.error("Error creating website:", createErr.response?.data || createErr.message);
          alert("Failed to create website.");
        }
      } else {
        console.error("Error adding password:", errorMsg || err.message);
        alert("Error adding password.");
      }
    }
  };  

  const handleUpdatePassword = async (e) => {
    e.preventDefault();

    const { website_name, old_pass, new_pass, confirm_pass } = updatePass;

    if (new_pass !== confirm_pass) {
      alert("New passwords do not match.");
      return;
    }

    if (old_pass === new_pass) {
      alert("New password must be different than the old password.");
      return;
    }

    try {
      const response = await axios.put(`${API_BASE}/passwords/website`, {
        website_name,
        new_pass
      }, {
        withCredentials: true
      });

      alert(response.data.message);
      fetchPasswords();
      setUpdatePass({
        website_name: '',
        old_pass: '',
        new_pass: '',
        confirm_pass: ''
      });
    } catch (err) {
      console.error("Error updating password:", err.response?.data || err.message);
      alert("Failed to update password.");
    }
  };  

  const handleDeletePassword = async (e) => {
    e.preventDefault();

    const confirmed = window.confirm(`Are you sure you want to delete the password for ${deleteWebsite}? This cannot be undone.`);

    if (!confirmed) return;

    try {
      const response = await axios.delete(`${API_BASE}/passwords/website`, {
        data: { website_name: deleteWebsite }, 
        withCredentials: true
      });

      alert(response.data.message);
      setDeleteWebsite('');
      fetchPasswords();
    } catch (err) {
      console.error("Error deleting password:", err.response?.data || err.message);
      alert("Failed to delete password.");
    }
  };
  

  return (
    <div className="password-manager-container">

      <div className="password-section">
        <h3>View Password by Website</h3>
        <form onSubmit={handleRevealPassword}>
          <select
            value={selectedWebsite}
            onChange={(e) => {
              setSelectedWebsite(e.target.value);
              setRevealedPassword('');
            }}
            required
          >
            <option value="">Select Website</option>
            {passwords.map((entry, idx) => (
              <option key={idx} value={entry.website_name}>
                {entry.website_name}
              </option>
            ))}
          </select>
          <button type="submit">Reveal Password</button>
        </form>

        {revealedPassword && (
          <div className="revealed-password">
            <strong>Password:</strong> {revealedPassword}
          </div>
        )}
      </div>

      <h3>Add Website Password</h3>
      <form onSubmit={handleAddPassword}>
        <input
          type="text"
          placeholder="Website Name"
          value={newPass.website_name}
          onChange={(e) => setNewPass({ ...newPass, website_name: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Password"
          value={newPass.web_pass}
          onChange={(e) => setNewPass({ ...newPass, web_pass: e.target.value })}
          required
        />
        <button type="submit">Save</button>
      </form>

      <h3>Update Website Password</h3>
      <form onSubmit={handleUpdatePassword}>
        <select
          value={updatePass.website_name}
          onChange={(e) => setUpdatePass({ ...updatePass, website_name: e.target.value })}
          required
        >
          <option value="">Select Website</option>
          {passwords.map((entry, idx) => (
            <option key={idx} value={entry.website_name}>
              {entry.website_name}
            </option>
          ))}
        </select>
        <input
          type="password"
          placeholder="Old Password"
          value={updatePass.old_pass}
          onChange={(e) => setUpdatePass({ ...updatePass, old_pass: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="New Password"
          value={updatePass.new_pass}
          onChange={(e) => setUpdatePass({ ...updatePass, new_pass: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Confirm New Password"
          value={updatePass.confirm_pass}
          onChange={(e) => setUpdatePass({ ...updatePass, confirm_pass: e.target.value })}
          required
        />
        <button type="submit">Update</button>
      </form>

      <h3>Delete Website Password</h3>
      <form onSubmit={handleDeletePassword}>
        <select
          value={deleteWebsite}
          onChange={(e) => setDeleteWebsite(e.target.value)}
          required
        >
          <option value="">Select Website</option>
          {passwords.map((entry, idx) => (
            <option key={idx} value={entry.website_name}>
              {entry.website_name}
            </option>
          ))}
        </select>
        <button type="submit" style={{ backgroundColor: '#d9534f', color: 'white' }}>
          Delete Password
        </button>
      </form>

    </div>
  );
};

export default PasswordManager;