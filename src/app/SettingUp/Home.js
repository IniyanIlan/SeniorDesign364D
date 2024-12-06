// PirateGame.js

import React from 'react';
import { useNavigate } from "react-router";

const Home = () => {
  const navigate = useNavigate();

  const playButtonSound = () => {
    const audio = new Audio('/click_3.mp3');
    audio.play();
    // playButtonSound();
  };

  const handleEnterPlayGameButton = () => {
    playButtonSound();
    navigate('/NumberPlayer');
  };
  const handleRulesButton = () => {
    playButtonSound();
    navigate('/Rules');
  };
  const handleGameDemo = () => {
    playButtonSound();
    window.location.href = "https://www.youtube.com/watch?v=3HUFUgqmWy8";
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