
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Excavation = ({ chestList, currentPlayer, currentPlayerIndex, playerNames  }) => {
  const navigate = useNavigate();
  const [message, setMessage] = useState("");

  const handleGoldUpdate = async (amount) => {
    try {
        await axios.post("http://localhost:5001/update_gold", {
            playerName: currentPlayer,
            goldChange: amount
        });
        console.log(`Updated ${currentPlayer}'s gold by ${amount}`);
    } catch (error) {
        console.error("Error updating gold:", error);
    }
  };
  const playButtonSound = () => {
    const audio = new Audio('/click_3.mp3');
    audio.play();
    // playButtonSound();
  };
  const playGoldSound = () => {
    const audio = new Audio('/gold-louder.wav');
    audio.play();
    // playGoldSound();
  };

  const handleExcavate = async () => {
    playButtonSound();
    try {
      const response = await fetch("http://localhost:5001/excavate");
      const data = await response.json();
      console.log(data)

      if (response.ok) {
        // if (data.result === 1) {
        //   handleGoldUpdate(100);
        //   playGoldSound();
        //   navigate('/Excavate_Treasure', { 
        //     state: { 
        //       playerNames,
        //       currentPlayer, 
        //       currentPlayerIndex
        //     } 
        //   });  // Navigate to the treasure component
        // } else if (data.result === 0) {
          const randomNumber = Math.floor(Math.random() * (10 - 4 + 1)) + 4;
          navigate('/Excavate_Bomb', { 
            state: { 
              playerNames,
              currentPlayer, 
              currentPlayerIndex,
              randomNumber
            } 
          });
      } else {
        setMessage(data.message);  // Display error message if no more chests
      }
    } catch (error) {
      console.error("Error excavating chest:", error);
      setMessage("An error occurred.");
    }
  };

  return (
    <div>
      <button  className='button'onClick={handleExcavate}>Excavate</button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Excavation;