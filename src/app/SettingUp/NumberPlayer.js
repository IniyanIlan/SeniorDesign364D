import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const NumberPlayer = () => {
  const [numberOfPlayers, setNumberOfPlayers] = useState(1); // Default to 1 player
  const [chestList, setChestList] = useState([]);
  const navigate = useNavigate();
  const maxPlayers = 6;

  const handleSubmit = (event) => {
    event.preventDefault();
    if (numberOfPlayers <= maxPlayers) {
      fetch("http://localhost:5001/")
        .then((response) => response.json())
        .then((data) => {
          setChestList(data.chestList);
          // Navigate to PlayerEnterName with number of players and chestList
          navigate('/PlayerEnterName', { 
            state: { 
              numberOfPlayers: parseInt(numberOfPlayers, 10), 
              chestList: data.chestList // Pass chest list to next component
            } 
          }); 
        })
        .catch((error) => console.error("Error initializing chests:", error));
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
        <button className='button' type="submit" disabled={numberOfPlayers > maxPlayers}>Next</button>
        {numberOfPlayers > maxPlayers && (
          <p style={{ color: 'red' }}>The maximum number of players is 6.</p>
        )}
      </form>
    </div>
  );
};

export default NumberPlayer;