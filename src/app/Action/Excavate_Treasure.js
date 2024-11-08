import React from 'react';
import { useState } from 'react';
import { useNavigate, useLocation } from "react-router";

function Excavate_Treasure () {
    const location = useLocation();
    const navigate = useNavigate();

    const { state } = useLocation();  // Get the playerNames from state
    const playerNames = state?.playerNames || [];

    const handleBackToGame = () => {
        navigate('/StartGame', { state: { playerNames } });  // Pass playerNames back to the game page
      };
    const handleClick = () => {
        navigate('/StartGame'); 
      };
    return(
        <div className='center-container'>
          <div className='centered-content'>
          <h1>you found treasure!</h1>
          <p>+ 100 gold</p>
          <button onClick={handleBackToGame}>Next Player</button>
          </div>
        </div>
    )
}

export default Excavate_Treasure;