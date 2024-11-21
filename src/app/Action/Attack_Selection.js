import React from "react";
import "./Attack_Selection.css";
import { useNavigate, useLocation } from "react-router";
import { useState, useEffect } from 'react';
import axios from 'axios';

function Attack_Selection() {
  const navigate = useNavigate();
  const location = useLocation();
  const [message, setMessage] = useState("");
  const { state } = location;
  const { attacker, defender, playerNames, currentPlayer, currentPlayerIndex } = state || {};
  const [attackerRoll, setAttackerRoll] = useState(0)
  const [defenderRoll, setDefenderRoll] = useState(0)
  const [attackerGold, setAttackerGold] = useState(0)
  const [defenderGold, setDefenderGold] = useState(0)

  
  const handleBackToGame = () => {
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
  console.log(playerNames)
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
  try{
    // const res = await axios.get("http://localhost:5001/trigger-dice");
    // setAttackerRoll(res.data.value)
    setAttackerRoll(6)

  }
  catch(error){
    console.error("Error during attack:", error);
    setAttackerRoll(0)
    setMessage("An error occurred.");
  }
}

const handleDefense = async () => {
  try{
    // const res = await axios.get("http://localhost:5001/trigger-dice");
    // setDefenderRoll(res.data.value)
    setDefenderRoll(1)

  }
  catch(error){
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
          <p>
            Gold:{" "}
            <input
              type="text"
              readOnly
              value={attackerGold}
              className="gold-input"
            />
          </p>
          <button className="button" onClick={handleAttack}>
            Attack!
          </button>
          {attackerRoll != 0 && <p>{attacker} rolled a {attackerRoll}</p>}
        </div>

        {/* Defender Section */}
        <div className="combat-card">
          <h2>Defender</h2>
          <p className="character-name">{defender}</p>
          <p>
            Gold:{" "}
            <input
              type="text"
              readOnly
              value={defenderGold}
              className="gold-input"
            />
          </p>
          <button className="button" onClick={handleDefense}>
            Defend!
          </button>
          {defenderRoll != 0 && <p>{defender} rolled a {defenderRoll}</p>}
        </div>
      </div>
      {/* change this to trigger dice */}
      <button className="button" onClick={handleBackToGame}>
        back to game
      </button>
      
    </div>
  );
}

export default Attack_Selection;
