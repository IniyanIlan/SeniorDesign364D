// PlayerNameEntry.js

import React, { useState } from 'react';
import {Link, useNavigate, useLocation} from 'react-router-dom';

const PlayerNameEntry = () => {
  const location = useLocation();
  const { numberOfPlayers } = location.state || {}; // Make sure to get numberOfPlayers from state
  const [playerNames, setPlayerNames] = useState(Array(numberOfPlayers).fill(''));
  const navigate = useNavigate();

  const handleInputChange = (index, event) => {
    const newPlayerNames = [...playerNames];
    newPlayerNames[index] = event.target.value;
    setPlayerNames(newPlayerNames);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    <Link 
      to={{
        pathname: "/StartGame",
        state: {playerNames} 
      }}/>
    navigate('/StartGame', { state: { playerNames } });
  };

  return (
    <div className="container">
      <h2 className="title"> Enter Player Names</h2>
      <form onSubmit={handleSubmit}>
        {playerNames.map((playerName, index) => ( // Renamed 'name' to 'playerName'
          <div key={index}>
            <label>Player {index + 1}:</label>
            <input
              type="text"
              value={playerName} // Updated 'name' to 'playerName'
              onChange={(event) => handleInputChange(index, event)}
              required
            />
          </div>
        ))}
        <button type="submit">Start Game</button>
      </form>
    </div>
  );
};

export default PlayerNameEntry;
