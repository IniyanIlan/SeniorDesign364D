import React from "react";
import "./Attack_Selection.css";
import { useNavigate, useLocation } from "react-router";
import { useState, useEffect } from 'react';
import axios from 'axios';

const playButtonSound = () => {
  const audio = new Audio('/click_3.mp3');
  audio.play();
  // playButtonSound();
};

//Fight_effect.wav
const playFightSound = () => {
  const audio = new Audio('/Fight_effect.wav');
  audio.play();
  // playFightSound();
};

function Attack_Selection() {
  const navigate = useNavigate();
  const location = useLocation();
  const [message, setMessage] = useState("");
  const { state } = location;
  const { attacker, defender, playerNames, currentPlayer, currentPlayerIndex } = state || {};
  const [attackerRoll, setAttackerRoll] = useState(null)
  const [defenderRoll, setDefenderRoll] = useState(null)
  const [attackerGold, setAttackerGold] = useState(null)
  const [defenderGold, setDefenderGold] = useState(null)

  
  const handleBackToGame = () => {
    playButtonSound();
    console.log("player names: ", playerNames)
    console.log("current player: ", currentPlayer)
    navigate('/TurnTracking', { state: { 
      playerNames, 
      currentPlayerIndex : (currentPlayerIndex + 1) % playerNames.length, 
      nextTurn: true } });
};

const handleGoldUpdate = async (amount, player) => {
  try {
      await axios.post("http://localhost:5001/update_gold", {
          playerName: player,
          goldChange: amount
      });
      console.log(`Updated ${player}'s gold by ${amount}`);
  } catch (error) {
      console.error("Error updating gold:", error.response?.data || error.message);
  }
};

const handleWinner = async () => {
  console.log("Handling winner")
  try {
      console.log("try success");
      const response = await fetch(`http://localhost:5001/attack/${attackerRoll}/${defenderRoll}`); // Call the backend API
      const data = await response.json(); // Parse the JSON response
      console.log(response);

      if (response.ok) {
        console.log(data.result)
          setAttackerGold(data.result)
          setDefenderGold(data.result * -1)
          const attackG = data.result
          const defendG = data.result * -1
          handleGoldUpdate(attackG, attacker)
          handleGoldUpdate(defendG, defender)

          // Determine winner and loser gold based on backend result
          if (data.result > 0) {
              alert(attacker + " has successfully looted the defender!")
          } else if (data.result < 0) {
              alert(defender + " has successfully defended against the attack!")
          } else {
              alert("The tide sways both sides. " + attacker + " has been given a reward for their courage.")
              setAttackerGold(50)
              handleGoldUpdate(50, attacker)
          }
      } else {
          setMessage("Attack failed.");
      }
  } catch (error) {
      console.error("Error during attack:", error);
      setMessage("An error occurred.");
  }
};

const handleAttack = async () => {
  playFightSound();
  try{
    console.log("From attack_selection.js " + defender)
    const res = await axios.get("http://localhost:5001/trigger-dice");
    setAttackerRoll(res.data.value)
    // setAttackerRoll(6)

  }
  catch(error){
    if (error.code === 'ECONNABORTED' || error.response?.status === 408) {
      setMessage("Timeout error: Click the attack button to try again!");
  }
    console.error("Error during attack:", error);
    setAttackerRoll(0)
    setMessage("An error occurred.");
  }
}

const handleDefense = async () => {
  playFightSound();
  try{
    const res = await axios.get("http://localhost:5001/trigger-dice");
    setDefenderRoll(res.data.value)
    // setDefenderRoll(1)

  }
  catch(error){
    console.error("Error during defense:", error);
    if (error.code === 'ECONNABORTED' || error.response?.status === 408) {
      setMessage("Timeout error: Click the defend button to try again!");
  }
    console.error("Error during attack:", error);
    setDefenderRoll(0)
    setMessage("An error occurred.");
  }
  
}

  useEffect(() => {
    if(attackerGold != 0 || defenderGold != 0){
      console.log("Changing gold amount")
    }

  },[attackerGold, defenderGold]);

  useEffect(() => {
    if(attackerRoll != 0 && defenderRoll != 0){
      console.log("Calculating Winner")
      handleWinner()
    }

  },[attackerRoll, defenderRoll]);

  return (
    <div className="combat-container">
      <h1>Combat!</h1>
      <div className="combat-columns">
        {/* Attacker Section */}
        <div className="combat-card">
          <h2>Attacker</h2>
          <p className="character-name">{attacker}</p>
          {attackerRoll && (
              <p>
              Gold:{" "}
              <input
                  type="text"
                  readOnly
                  value={attackerGold}
                  className="gold-input"
              />
              </p>
          )}
          <button className="button" disabled={attackerRoll != null} onClick={handleAttack}>
            Attack!
          </button>
          {attackerRoll != null && <p>{attacker} rolled a {attackerRoll}</p>}
        </div>

        {/* Defender Section */}
        <div className="combat-card">
          <h2>Defender</h2>
          <p className="character-name">{defender}</p>
          {defenderRoll && (
              <p>
              Gold:{" "}
              <input
                  type="text"
                  readOnly
                  value={defenderGold}
                  className="gold-input"
              />
              </p>
          )}
          <button className="button" disabled={defenderRoll} onClick={handleDefense}>
            Defend!
          </button>
          {defenderRoll != null && <p>{defender} rolled a {defenderRoll}</p>}
        </div>
      </div>
      {/* change this to trigger dice */}
      <button className="button" onClick={handleBackToGame}>
        Back to game
      </button>
      
    </div>
  );
}

export default Attack_Selection;
