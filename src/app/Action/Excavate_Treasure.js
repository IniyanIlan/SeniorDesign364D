import React from 'react';
import { useState } from 'react';
import { useNavigate, useLocation } from "react-router";
import './Excavate.css'

function Excavate_Treasure () {
    const location = useLocation();
    const navigate = useNavigate();

    const { state } = useLocation();  // Get the playerNames from state
    const playerNames = state.playerNames || [];
    const currentPlayer = state.currentPlayer;
    const currentPlayerIndex = state.currentPlayerIndex;

    const playButtonSound = () => {
      const audio = new Audio('/click_3.mp3');
      audio.play();
      // playButtonSound();
    };
    const handleBackToGame = () => {
      playButtonSound();
      navigate('/TurnTracking', { state: { 
        playerNames, 
        currentPlayerIndex : (currentPlayerIndex + 1) % playerNames.length, 
        nextTurn: true } });
}; 
      
    const handleClick = () => {
        navigate('/StartGame'); 
      };
    return(
        <div className='center-container'>
          <div className='centered-content'>
          <h1>you found treasure!</h1>
          <img
                className = "chest-img"
                src="/treasure-chest.jpg" 
                alt="Board"
          />
          <button onClick={handleBackToGame}>Next Player</button>
          </div>
        </div>
    )
}

export default Excavate_Treasure;