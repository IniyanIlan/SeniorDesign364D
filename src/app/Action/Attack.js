import React, { useState } from 'react';
import { useNavigate } from "react-router";

const Attack = ({ attackPlayers, playerNames, currentPlayer, currentPlayerIndex }) => {
    const [message, setMessage] = useState(""); // State to store the attack message
    const [selectedPlayer, setSelectedPlayer] = useState(attackPlayers[0]);
    const navigate = useNavigate();

    const handlePlayerChange = (event) => {
        setSelectedPlayer(event.target.value);
    };

    const handleAttackClick = async () => {
        console.log(playerNames)
        try {
            const response = await fetch("http://localhost:5001/attack"); // Call the backend API
            const data = await response.json(); // Parse the JSON response
            if (response.ok) {
                // Set the attacker and defender based on currentPlayer and selectedPlayer
                const attacker = currentPlayer;
                const defender = selectedPlayer;

                // Gold values (these could be dynamic, but I’m setting them as 0 for now)
                const attackerGold = data.result;
                const defenderGold = data.result * -1;
                const playerlist = playerNames;
                const currentIndex = currentPlayerIndex;

                console.log("attacker:", attacker);
                console.log("defender:", defender);
                console.log("Passing playerNames to Attack:", playerNames);
                // Navigate to Attack_Selection and pass the state
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
            <select value={selectedPlayer} onChange={handlePlayerChange} className="dropdown">
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
