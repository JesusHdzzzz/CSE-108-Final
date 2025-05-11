import React, { useEffect, useState } from 'react';
import axios from 'axios';

const cardManager = () => {
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
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Your Cards</h2>
      {cards.length === 0 ? (
        <p>No cards saved.</p>
      ) : (
        <ul className="space-y-2">
          {cards.map((card, idx) => (
            <li key={idx} className="p-4 border rounded-xl bg-white shadow">
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

export default cardManager;