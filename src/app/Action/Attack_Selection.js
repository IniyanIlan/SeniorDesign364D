import React from "react";
import "./Attack_Selection.css";
import { useNavigate, useLocation } from "react-router";

function Attack_Selection() {
  const navigate = useNavigate();
  const location = useLocation();
  const { state } = location;
  const { attacker, defender, attackerGold, defenderGold, playerNames, currentPlayer, currentPlayerIndex } = state || {};
  const handleBackToGame = () => {
    console.log("player names: ", playerNames)
    console.log("current player: ", currentPlayer)
    navigate('/TurnTracking', { state: { 
      playerNames, 
      currentPlayerIndex : (currentPlayerIndex + 1) % playerNames.length, 
      nextTurn: true } });
};
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

      {/* change this to trigger dice */}
      <button className="button" onClick={handleBackToGame}>
        back to game
      </button>
    </div>
  );
}

export default Attack_Selection;
