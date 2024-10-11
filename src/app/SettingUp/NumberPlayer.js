import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const NumberPlayer = () => {
  const [numberOfPlayers, setNumberOfPlayers] = useState(1); // Default to 1 player
  const navigate = useNavigate();
  const maxPlayers = 6;

  const handleSubmit = (event) => {
    event.preventDefault();
    if (numberOfPlayers <= maxPlayers) {
      navigate('/PlayerEnterName', { state: { numberOfPlayers: parseInt(numberOfPlayers, 10) } });
    }
  };

  return (
    <div className="container">
      <h2 className="title"> Enter Number of Players (Max 6)</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Number of Players:
          <input
            type="number"
            min="1"
            max={maxPlayers}
            value={numberOfPlayers}
            onChange={(e) => setNumberOfPlayers(e.target.value)}
            required
          />
        </label>
        <button type="submit" disabled={numberOfPlayers > maxPlayers}>Next</button>
        {numberOfPlayers > maxPlayers && (
          <p style={{ color: 'red' }}>The maximum number of players is 6.</p>
        )}
      </form>
    </div>
  );
};

export default NumberPlayer;