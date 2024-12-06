// TurnTracking.js

import React, { useState, useEffect } from 'react';
import { useLocation , useNavigate } from 'react-router-dom';
import '../Tracking/Game.css';
import axios from 'axios';
import Trigger from '../Action/TriggerDice'


const TurnTracking = () => {
  const location = useLocation();
  const { playerNames, chestList} = location.state || {};
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState(0); // Track current player index
  const navigate = useNavigate();
  const [pipValue, setPips] = useState(0)

  const playButtonSound = () => {
    const audio = new Audio('/click_3.mp3');
    audio.play();
    // playButtonSound();
  };

  // const handleRollDice = async () => {
  //   playButtonSound()
  //   console.log("handleRollDice player:", playerNames[currentPlayerIndex]);
  //   try{
  //     const res = await axios.get("http://localhost:5001/trigger-dice")
  //   }
  //   catch(e){
  //     console.log("Error fetching dice value")
  //   }
  //   navigate('/StartGame', { state: { playerNames, currentPlayerIndex, nextTurn: false, chestList} });
  // };
  const handleRollDice = async () => {
    // playButtonSound()
    console.log("handleRollDice player:", playerNames[currentPlayerIndex]);
    try{
      const res = await axios.get("http://localhost:5001/trigger-dice")
      setPips(res.data.value)
      console.log("Dice value:", res.data.value)
    }
    catch(error){
      if (error.code === 'ECONNABORTED' || error.response?.status === 408) {
          console.error("Timeout error: The request took too long to complete.");
      } 
      else{
          console.error("Error: unable to recieve dice request");
      }
    }     
  };

  useEffect(() => {
    if(pipValue !== 0){
        navigate('/StartGame', { state: { playerNames, currentPlayerIndex, nextTurn: false, chestList, pipValue} });
    }
  },[pipValue]);


  // const handleTrigger = async () => {
  //     playButtonSound()
  //     console.log("Starting Dice Reader")
  //     try{
  //         const res = await axios.get("http://localhost:5001/trigger-dice")
  //         setNumPips(res.data.value)
  //         console.log("Dice value:", res.data.value)
  //     }
  //     catch(error){
  //         if (error.code === 'ECONNABORTED' || error.response?.status === 408) {
  //             console.error("Timeout error: The request took too long to complete.");
  //         } 
  //         else{
  //             console.error("Error: unable to recieve dice request");
  //         }
  //         setNumPips(0);  // Set default or handle accordingly
  //     }
  // }

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
        {/* <Trigger></Trigger> */}
      </div>
    </div>
    
  );
};

export default TurnTracking;