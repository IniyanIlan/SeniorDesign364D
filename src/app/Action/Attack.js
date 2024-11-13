import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";


const Attack = ({ attackPlayers, playerNames, currentPlayer, currentPlayerIndex }) => {
    const [message, setMessage] = useState(""); // State to store the attack message
    const [selectedPlayer, setSelectedPlayer] = useState(attackPlayers[0]);
    const navigate = useNavigate();

    const handlePlayerChange = (event) => {
        setSelectedPlayer(event.target.value);
    };

    const handleAttackClick = () => {
        const attacker = currentPlayer;
        const defender = selectedPlayer;
        navigate('/Attack_Selection', { 
            state: {
                attacker,
                defender,
                playerNames,
                currentPlayer,
                currentPlayerIndex
            } 
        });
    }
    
          // Pass the state to Attack_Selection
    
    
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
