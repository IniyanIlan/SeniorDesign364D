// PirateGame.js

import React from 'react';
import { useNavigate } from "react-router";

const Home = () => {
  const navigate = useNavigate();
  const handleEnterPlayGameButton = () => {
    // Navigate to another page
    navigate('/PlayerEnterName');
  };
  const handleRulesButton = () => {
    // Navigate to another page
    navigate('/Rules');
  };
  const handleGameDemo = () => {
    // Navigate to another page
    window.location.href = "https://www.youtube.com/watch?v=eR07kFFZ_iU";
  };
  return (
    <div className="container">
      <h1 className="title">Welcome to Pirate Adventure!</h1>
      <h1 className="title">Legends of the Lost Sea: Tides of Treachery</h1>
      <img
        className="pirate-image"
        src="/pirate-character.jpg" 
        alt="Pirate Character"
      />
      <button className="button" onClick={handleEnterPlayGameButton}>Start Game</button>
      <button className="button" onClick={handleRulesButton}>Game Rules</button>
      <button className="button" onClick={handleGameDemo}>Game Demo</button>
    </div>
  );
};

export default Home;