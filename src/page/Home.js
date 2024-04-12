// PirateGame.js

import React from 'react';
import { Navigate } from 'react-router-dom';
import { useNavigate } from "react-router";

const Home = () => {
  const navigate = useNavigate();
  const handleEnterPlayGameButton = () => {
    // Navigate to another page
    navigate('/PlayerEnterName');
  };
  return (
    <div className="container">
      <h1 className="title">Welcome to Pirate Adventure!</h1>
      <img
        className="pirate-image"
        src="/pirate-character.jpg" // Placeholder image URL
        alt="Pirate Character"
      />
      <button className="button" onClick={handleEnterPlayGameButton}>
        Enter Player Name
      </button>
    </div>
  );
};

export default Home;
