import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './cardManager.css';

const API_BASE = process.env.REACT_APP_API_BASE_URL;

const CardManager = () => {
  const [cards, setCards] = useState([]);

  const [newCard, setNewCard] = useState({
    cardholder_name: '',
    card_number: '',
    card_type: '',
    expiration_date: '',
    cvv: '',
    billing_address: ''
  });  

  const [updateCard, setUpdateCard] = useState({
    card_number: '',
    cardholder_name: '',
    card_type: '',
    expiration_date: '',
    cvv: '',
    billing_address: ''
  });

  const [deleteNumber, setDeleteNumber] = useState('');

  useEffect(() => {
    fetchCards();
  }, []);

  const fetchCards = async () => {
    try {
      const response = await axios.get(`${API_BASE}/cards/`, {
        withCredentials: true,
      });
      const data = response.data;

      if (data.cards) {
        setCards(data.cards);
      } else {
        console.warn("No cards found in response:", data);
        setCards([]);
      }
    } catch (err) {
      console.error('Error fetching cards:', err);
    }
  };

  const handleAddCard = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_BASE}/cards/`, newCard, {
        withCredentials: true,
      });
      console.log(response.data.message);
      fetchCards(); // refresh the list
      setNewCard({ cardholder_name: '', card_number: '', card_type: '', expiration_date: '', cvv: '', billing_address: '' });
    } catch (err) {
      console.error('Error adding card:', err.response?.data || err.message);
    }
  };  

  const handleUpdateCard = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.put(`${API_BASE}/cards/`, updateCard, {
        withCredentials: true,
      });
      console.log(response.data.message);
      fetchCards();
    } catch (err) {
      console.error('Error updating card:', err.response?.data || err.message);
    }
  };

  const handleDeleteCard = async (e) => {
    e.preventDefault();

    const selectedCard = cards.find(c => c.card_number === deleteNumber);
    if (!selectedCard) {
      alert("Please select a valid card.");
      return;
    }

    const confirmDelete = window.confirm(
      `Are you sure you want to delete the card ending in ${deleteNumber.slice(-4)}?`
    );

    if (!confirmDelete) return;

    try {
      const response = await axios.delete(`${API_BASE}/cards/`, {
        data: { card_number: deleteNumber }, 
        withCredentials: true,
      });
      console.log(response.data.message);
      fetchCards();
      setDeleteNumber('');
    } catch (err) {
      console.error('Error deleting card:', err.response?.data || err.message);
    }
  };
  

  return (
    <div className="card-manager-container">
      <h2 className="card-manager-title">Your Cards</h2>
      {cards.length === 0 ? (
        <p>No cards saved.</p>
      ) : (
        <ul className="card-list">
          {cards.map((card, idx) => (
            <li key={idx} className="card-item">
              <div><strong>Cardholder:</strong> {card.cardholder_name}</div>
              <div><strong>Number:</strong> {card.card_number}</div>
              <div><strong>Type:</strong> {card.card_type}</div>
              <div><strong>Expires:</strong> {card.expiration_date}</div>
              <div><strong>Billing Address:</strong> {card.billing_address}</div>
            </li>
          ))}
        </ul>
      )}

      <h3>Add a New Card</h3>
        <form onSubmit={handleAddCard}>
          <input type="text" placeholder="Cardholder Name" value={newCard.cardholder_name} onChange={e => setNewCard({...newCard, cardholder_name: e.target.value})} required />
          <input type="text" placeholder="Card Number" value={newCard.card_number} onChange={e => setNewCard({...newCard, card_number: e.target.value})} required />
          <select
            value={newCard.card_type}
            onChange={e => setNewCard({ ...newCard, card_type: e.target.value })}
            required>
            <option value="">Select Card Type</option>
            <option value="Visa">Visa</option>
            <option value="MasterCard">MasterCard</option>
            <option value="American Express">American Express</option>
          </select>
          <input type="month" placeholder="Expiration (YYYY-MM)" value={newCard.expiration_date} onChange={e => setNewCard({...newCard, expiration_date: e.target.value})} required />
          <input type="text" placeholder="CVV" value={newCard.cvv} onChange={e => setNewCard({...newCard, cvv: e.target.value})} required />
          <input type="text" placeholder="Billing Address" value={newCard.billing_address} onChange={e => setNewCard({...newCard, billing_address: e.target.value})} required />
          <button type="submit">Add Card</button>
        </form>

      <h3>Update Card</h3>
      <form onSubmit={handleUpdateCard}>
        <select
          value={updateCard.card_number}
          onChange={(e) => {
            const selected = cards.find(c => c.card_number === e.target.value);
            if (selected) {
              setUpdateCard({
                ...updateCard,
                card_number: selected.card_number,
                cardholder_name: selected.cardholder_name,
                card_type: selected.card_type,
                expiration_date: selected.expiration_date,
                cvv: '', // you probably don't store this, so let them input
                billing_address: selected.billing_address
              });
            }
          }}
          required
        >
          <option value="">Select Card to Update</option>
          {cards.map((card, idx) => (
            <option key={idx} value={card.card_number}>
              {card.cardholder_name} ••••{card.card_number.slice(-4)} ({card.card_type})
            </option>
          ))}
        </select>

        <input type="text" placeholder="Cardholder Name" value={updateCard.cardholder_name} onChange={e => setUpdateCard({ ...updateCard, cardholder_name: e.target.value })} required />

        <select value={updateCard.card_type} onChange={e => setUpdateCard({ ...updateCard, card_type: e.target.value })} required>
          <option value="">Select Card Type</option>
          <option value="Visa">Visa</option>
          <option value="MasterCard">MasterCard</option>
          <option value="American Express">American Express</option>
        </select>

        <input type="month" placeholder="Expiration Date" value={updateCard.expiration_date} onChange={e => setUpdateCard({ ...updateCard, expiration_date: e.target.value })} required />

        <input type="text" placeholder="CVV" value={updateCard.cvv} onChange={e => setUpdateCard({ ...updateCard, cvv: e.target.value })} />

        <input type="text" placeholder="Billing Address" value={updateCard.billing_address} onChange={e => setUpdateCard({ ...updateCard, billing_address: e.target.value })} required />

        <button type="submit">Update Card</button>
      </form>

      <h3>Delete Card</h3>
      <form onSubmit={handleDeleteCard}>
        <select
          value={deleteNumber}
          onChange={(e) => setDeleteNumber(e.target.value)}
          required
        >
          <option value="">Select Card to Delete</option>
          {cards.map((card, idx) => (
            <option key={idx} value={card.card_number}>
              {card.cardholder_name} ••••{card.card_number.slice(-4)} ({card.card_type})
            </option>
          ))}
        </select>

        <button type="submit">Delete</button>
      </form>


    </div>
  );
};

export default CardManager;
