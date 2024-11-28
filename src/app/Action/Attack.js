import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";

const Attack = ({ attackPlayers, playerNames, currentPlayer, currentPlayerIndex }) => {
    const [message, setMessage] = useState(""); // State to store the attack message
    const [selectedPlayer, setSelectedPlayer] = useState(attackPlayers[0]);
    const navigate = useNavigate();

    const handlePlayerChange = (event) => {
        console.log("From Attack.js playerChange");
        console.log(event.target.value);
        setSelectedPlayer(event.target.value);
    };

    const handleAttackClick = () => {
        console.log("From Attack.js attackclick");
        console.log(selectedPlayer);
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
    useEffect(() => {
            if (attackPlayers && attackPlayers.length > 0) {
                setSelectedPlayer(attackPlayers[0]); // Set to the first valid player
            }
    }, [attackPlayers]);
    
    return (
        <div>
            <select value={selectedPlayer} onChange={handlePlayerChange} className="button">
                {console.log("From render dropdown " + selectedPlayer)}
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
