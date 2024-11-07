import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Winner.css';

const Winner = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { winner } = location.state || {};

  return (
    <div className="winner-container">
      <h1>Congratulations, captain {winner}!</h1>
      <p className="congrats-message">You’ve conquered the seas and claimed the treasure! </p>
      <p className="congrats-message">Your name will echo through the tides as a true legend of the Lost Sea!</p>
      <button className="play-again-button" onClick={() => navigate('/')}>
        Play Again
      </button>
    
    </div>
  );
};

export default Winner;