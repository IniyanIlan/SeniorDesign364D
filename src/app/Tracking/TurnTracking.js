// TurnTracking.js

import React, { useState, useEffect } from 'react';
import { useLocation , useNavigate } from 'react-router-dom';
import '../Tracking/Game.css';
import axios from 'axios';


const TurnTracking = () => {
  const location = useLocation();
  const { playerNames, chestList} = location.state || {};
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState(0); // Track current player index
  const navigate = useNavigate();

  const playButtonSound = () => {
    const audio = new Audio('/click_3.mp3');
    audio.play();
    // playButtonSound();
  };

  const handleRollDice = () => {
    playButtonSound()
    console.log("handleRollDice player:", playerNames[currentPlayerIndex]);
    navigate('/StartGame', { state: { playerNames, currentPlayerIndex, nextTurn: false, chestList} });
  };

  // useEffect(() => {
  //   if (location.state.nextTurn) {
  //     console.log("useEffect: currentPlayerIndex:", location.state.currentPlayerIndex);
  //     setCurrentPlayerIndex(location.state.currentPlayerIndex);
  //   }
  // }, [location.state.nextTurn]);

  useEffect(() => {
    const checkForWinner = async () => {
      try {
        const response = await axios.get("http://localhost:5001/get_winner");
        const { winner } = response.data;

        if (winner) {
          console.log("Winner found:", winner);
          navigate('/Winner', { state: { winner } });
        } else {
          console.log("useEffect: currentPlayerIndex:", location.state.currentPlayerIndex);
          setCurrentPlayerIndex(location.state.currentPlayerIndex); // Continue to next player
        }
      } catch (error) {
        console.error("Error checking for winner:", error);
      }
    };

    if (location.state.nextTurn) {
      checkForWinner(); // Call /get_winner if it's the next turn
    }
  }, [location.state.nextTurn]);


  return (
    <div>
      <div className = "banner">
                <a href="/Rules" target="_blank">Rule Book</a>
                {/* <a href="/StartGame">Game Log</a> */}
                <a href = "/NumberPlayer">Restart Game</a>
                <a href = "/" className = "quit">Quit</a>
      </div>
      <div className="game-columns">
        <h2>Welcome to the Game!</h2>
        <p>{playerNames[currentPlayerIndex]}, it's your turn. Roll the dice!</p>
        <button className="button" onClick={handleRollDice}>Roll Dice</button>
      </div>
    </div>
    
  );
};

export default TurnTracking;