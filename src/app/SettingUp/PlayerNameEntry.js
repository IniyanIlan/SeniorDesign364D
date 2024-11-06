// PlayerNameEntry.js

import React, { useState } from 'react';
import {useNavigate, useLocation} from 'react-router-dom';
import axios from 'axios';

const PlayerNameEntry = () => {
  const location = useLocation();
  const { numberOfPlayers, chestList } = location.state || {}; // Make sure to get numberOfPlayers from state
  const [playerNames, setPlayerNames] = useState(Array(numberOfPlayers).fill(''));
  const navigate = useNavigate();

  const handleInputChange = (index, event) => {
    const newPlayerNames = [...playerNames];
    newPlayerNames[index] = event.target.value;
    setPlayerNames(newPlayerNames);
  };

  // const cameraInit = async () =>{
  //   console.log("Intializing camera")
  //   try{
  //     const res = axios.get("http://localhost:5001/intialize-picam")
  //   }
  //   catch(error){
  //     console.error("Error setting up camera", error);
  //   }
  // }


  // const handleSubmit = async (event) => {
  //   event.preventDefault();
  //   // await cameraInit();
  //   navigate('/TurnTracking', { 
  //     state: { 
  //       playerNames,   // Pass player names to Game.js
  //       chestList      // Also pass the chest list to Game.js
  //     } 
  //   });
  // };
  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      await axios.post("http://localhost:5001/init_leaderboard", { playerNames });
      navigate('/TurnTracking', { 
        state: { 
          playerNames,  
          chestList
        }
      });
    } catch (error) {
      console.error("Error initializing players on backend:", error);
    }
  };

  return (
    <div className="container">
      <h2 className="title"> Enter Player Names</h2>
      <form onSubmit={handleSubmit}>
        {playerNames.map((playerName, index) => ( // Renamed 'name' to 'playerName'
          <div key={index}>
            <label>Player {index + 1}:</label>
            <input
              type="text"
              value={playerName} // Updated 'name' to 'playerName'
              onChange={(event) => handleInputChange(index, event)}
              required
            />
          </div>
        ))}
        <button className='button' type="submit">Start Game</button>
      </form>
    </div>
  );
};

export default PlayerNameEntry;
