import React from 'react';
import { useState } from 'react';
import { useNavigate, useLocation } from "react-router";

const Excavate_Bomb = () => {
    const navigate = useNavigate();
    const { state } = useLocation();  // Get data passed from Excavation
    const playerNames = state.playerNames || [];
    const currentPlayer = state.currentPlayer;
    const currentPlayerIndex = state.currentPlayerIndex;

    const handleBackToGame = () => {
        navigate('/TurnTracking', { state: { 
            playerNames, 
            currentPlayerIndex : (currentPlayerIndex + 1) % playerNames.length, 
            nextTurn: true } });
    }; 
    return(
        <div>
            <h1 className='title'>you found a bomb!</h1>
            <button onClick={handleBackToGame}>Back to Game</button>
        </div>
    )
}

export default Excavate_Bomb;