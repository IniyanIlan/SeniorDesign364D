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

const handleAttack = async () => {
  console.log(playerNames)
  try {
      console.log("try success");
      const response = await fetch("http://localhost:5001/attack"); // Call the backend API
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
              alert("The tide has favored both sides")
          }
      } else {
          setMessage("Attack failed.");
      }
  } catch (error) {
      console.error("Error during attack:", error);
      setMessage("An error occurred.");
  }
};

  useEffect(() => {
    if(attackerGold != 0 || defenderGold != 0){
      console.log("Changing god amount")
    }

  },[attackerGold, defenderGold]);

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
        </div>
      </div>
      <button className="button" onClick={handleAttack}>
        Attack!
      </button>

      {/* change this to trigger dice */}
      <button className="button" onClick={handleBackToGame}>
        back to game
      </button>
    </div>
  );
}

export default Attack_Selection;
