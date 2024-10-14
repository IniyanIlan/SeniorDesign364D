import React from 'react';
import { useState } from 'react';
import { useNavigate, useLocation } from "react-router";

const Excavate_Bomb = () => {
    const navigate = useNavigate();

    const { state } = useLocation();  // Get the playerNames from state
    const playerNames = state?.playerNames || [];

    const handleBackToGame = () => {
        navigate('/StartGame', { state: { playerNames } });  // Pass playerNames back to the game page
      };
    return(
        <div>
            <h1 className='title'>you found a bomb!</h1>
            <button onClick={handleBackToGame}>Back to Game</button>
        </div>
    )
}

export default Excavate_Bomb;