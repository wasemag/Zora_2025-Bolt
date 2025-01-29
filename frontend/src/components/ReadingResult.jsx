import React from 'react';

function ReadingResult({ reading, cards, selectedCardIds }) {
  if (!reading) {
    return <p>No reading available.</p>;
  }

  const selectedCardDetails = selectedCardIds.map(id => cards.find(card => card.id === id));

  return (
    <div className="reading-result bg-white p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Your Tarot Reading</h2>
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-2">Selected Cards:</h3>
        <div className="flex gap-4">
          {selectedCardDetails.map(card => (
            <div key={card.id} className="flex flex-col items-center">
              <img src={card.image_url} alt={card.name} className="w-32 rounded-md mb-2" />
              <p className="text-sm font-medium text-center">{card.name}</p>
            </div>
          ))}
        </div>
      </div>
      <div className="interpretation">
        <h3 className="text-lg font-semibold mb-2">Interpretation:</h3>
        <p>{reading.interpretation}</p>
      </div>
    </div>
  );
}

export default ReadingResult;
