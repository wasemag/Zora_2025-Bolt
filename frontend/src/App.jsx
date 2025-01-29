import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import axios from 'axios';
import './App.css';
import CardDisplay from './components/CardDisplay';
import ReadingForm from './components/ReadingForm';
import ReadingResult from './components/ReadingResult';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [cards, setCards] = useState([]);
  const [selectedCards, setSelectedCards] = useState([]);
  const [reading, setReading] = useState(null);
  const [question, setQuestion] = useState('');
  const [userInfo, setUserInfo] = useState({ name: '', dob: '', gender: '' });

  useEffect(() => {
    axios.get(`${API_URL}/api/cards`)
      .then(response => {
        setCards(response.data);
      })
      .catch(error => {
        console.error("Error fetching cards:", error);
      });
  }, []);

  const handleCardSelect = (cardId) => {
    if (selectedCards.includes(cardId)) {
      setSelectedCards(selectedCards.filter(id => id !== cardId));
    } else if (selectedCards.length < 3) { // Limit to 3 cards for a simple reading
      setSelectedCards([...selectedCards, cardId]);
    }
  };

  const handleFormSubmit = async () => {
    try {
      const response = await axios.post(`${API_URL}/api/reading`, {
        question: question,
        selected_cards: selectedCards,
        user_name: userInfo.name,
        dob: userInfo.dob,
        gender: userInfo.gender
      });
      setReading(response.data);
    } catch (error) {
      console.error("Error creating reading:", error);
      if (error.response) {
        console.error("Response data:", error.response.data);
        console.error("Response status:", error.response.status);
      }
    }
  };

  return (
    <Router>
      <div className="App bg-gray-100 min-h-screen p-4">
        <header className="bg-white shadow-md p-4 mb-4">
          <h1 className="text-2xl font-bold text-gray-800">Simple Tarot Reading</h1>
        </header>
        <Routes>
          <Route path="/" element={
            <div className="flex flex-col md:flex-row">
              <div className="md:w-1/2 p-4">
                <ReadingForm
                  question={question}
                  setQuestion={setQuestion}
                  userInfo={userInfo}
                  setUserInfo={setUserInfo}
                  onSubmit={handleFormSubmit}
                  selectedCards={selectedCards}
                />
              </div>
              <div className="md:w-1/2 p-4">
                <CardDisplay
                  cards={cards}
                  selectedCards={selectedCards}
                  onCardSelect={handleCardSelect}
                />
              </div>
            </div>
          } />
          <Route path="/reading-result" element={<ReadingResult reading={reading} cards={cards} selectedCardIds={selectedCards} />} />
        </Routes>
        {reading && <button onClick={() => { setReading(null); setSelectedCards([]); setQuestion(''); }} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4">Do Another Reading</button>}
      </div>
    </Router>
  );
}

export default App;
