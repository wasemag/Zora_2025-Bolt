import React from 'react';

function CardDisplay({ cards, selectedCards, onCardSelect }) {
  return (
    <div className="card-display bg-white p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Select Your Cards (Max 3)</h2>
      <div className="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
        {cards.map(card => (
          <div
            key={card.id}
            className={`card cursor-pointer rounded border-2 ${selectedCards.includes(card.id) ? 'border-blue-500' : 'border-transparent'} hover:shadow-md transition-shadow duration-200`}
            onClick={() => onCardSelect(card.id)}
          >
            <img src={card.image_url} alt={card.name} className="rounded-t w-full block" />
            <div className="p-2 text-center">
              <p className="text-sm font-medium">{card.name}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CardDisplay;
