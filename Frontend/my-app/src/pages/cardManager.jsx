import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './cardManager.css';


const CardManager = () => {
  const [cards, setCards] = useState([]);

  useEffect(() => {
    fetchCards();
  }, []);

  const fetchCards = async () => {
    try {
      const response = await axios.get('/cards');
      setCards(response.data.cards);
    } catch (err) {
      console.error('Error fetching cards:', err);
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
    </div>
  );
};

export default CardManager;