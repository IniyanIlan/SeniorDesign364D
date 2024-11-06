// TurnTracking.js

import React, { useState, useEffect } from 'react';
import { useLocation , useNavigate } from 'react-router-dom';
import '../Tracking/Game.css';

const TurnTracking = () => {
  const location = useLocation();
  const { playerNames, chestList} = location.state || {};
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState(0); // Track current player index
  const navigate = useNavigate();

  const handleRollDice = () => {
    console.log("handleRollDice player:", playerNames[currentPlayerIndex]);
    navigate('/StartGame', { state: { playerNames, currentPlayerIndex, nextTurn: false, chestList} });
  };

  useEffect(() => {
    if (location.state.nextTurn) {
      console.log("useEffect: currentPlayerIndex:", location.state.currentPlayerIndex);
      setCurrentPlayerIndex(location.state.currentPlayerIndex);
    }
  }, [location.state.nextTurn]);

  return (
    <div>
      <div className = "banner">
                <a href="/Rules" target="_blank">Rule Book</a>
                <a href="/StartGame">Game Log</a>
                <a href = "/NumberPlayer">Restart Game</a>
                <a href = "/" className = "quit">Quit</a>
      </div>
      <div className="game-container">
        <h2>Welcome to the Game!</h2>
        <p>{playerNames[currentPlayerIndex]}, it's your turn. Roll the dice!</p>
        <button onClick={handleRollDice}>Roll Dice</button>
      </div>
    </div>
    
  );
};

export default TurnTracking;