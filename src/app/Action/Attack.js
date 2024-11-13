import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';

const Attack = ({ attackPlayers, playerNames, currentPlayer, currentPlayerIndex }) => {
    const [message, setMessage] = useState(""); // State to store the attack message
    const [selectedPlayer, setSelectedPlayer] = useState(attackPlayers[0]);
    const navigate = useNavigate();

    const handlePlayerChange = (event) => {
        setSelectedPlayer(event.target.value);
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

    const handleAttackClick = async () => {
        console.log(playerNames)
        try {
            console.log("try success");
            const response = await fetch("http://localhost:5001/attack"); // Call the backend API
            const data = await response.json(); // Parse the JSON response
            console.log(response);
    
            if (response.ok) {
                // Set attacker and defender based on currentPlayer and selectedPlayer
                const attacker = currentPlayer;
                const defender = selectedPlayer;
    
                // Determine winner and loser gold based on backend result
                let attackerGold, defenderGold;
                if (data.result > 0) {
                    attackerGold = data.result; // Attacker wins, positive gold value
                    defenderGold = data.result * -1; // Defender loses, negative gold
                    handleGoldUpdate(attackerGold, currentPlayer)
                    handleGoldUpdate(defenderGold, selectedPlayer)
                } else if (data.result < 0) {
                    attackerGold = data.result * -1; // Attacker loses, negative gold
                    defenderGold = data.result; // Defender wins, positive gold value
                    handleGoldUpdate(attackerGold, currentPlayer)
                    handleGoldUpdate(defenderGold, selectedPlayer)
                } else {
                    attackerGold = 0; // Tie case, both gold values are zero
                    defenderGold = 0;
                }
    
                // Pass the state to Attack_Selection
                navigate('/Attack_Selection', { 
                    state: {
                        attacker,
                        defender,
                        attackerGold,
                        defenderGold,
                        playerNames,
                        currentPlayer,
                        currentPlayerIndex
                    } 
                });
            } else {
                setMessage("Attack failed.");
            }
        } catch (error) {
            console.error("Error during attack:", error);
            setMessage("An error occurred.");
        }
    };

    return (
        <div>
            <select value={selectedPlayer} onChange={handlePlayerChange} className="button">
                {attackPlayers.map((name) => (
                    <option key={name} value={name}>
                        {name}
                    </option>
                ))}
            </select>
            <button className='button' onClick={handleAttackClick}>Attack!</button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default Attack;
