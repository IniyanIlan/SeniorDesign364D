import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import Leaderboard from './Leaderboard';
import Excavation from '../Action/Excavation';
import Trigger from '../Action/TriggerDice';
import './Game.css';
import Attack from '../Action/Attack';


const Game = () => {
    const { state } = useLocation();
    const navigate = useNavigate();
    const { playerNames, currentPlayerIndex, chestList } = state;
    const currentPlayer = playerNames[currentPlayerIndex];
    const [leaderboard, setLeaderboard] = useState([]);
    const [otherPlayers, setOtherPlayers] = useState([]);

  useEffect(() => {
    // Fetch player scores from the backend
    const fetchScores = async () => {
      try {
        const response = await axios.get("http://localhost:5001/get_leaderboard");
        setLeaderboard(response.data);
        console.log("Fetch sorted_leaderboard data:", response.data);
      } catch (error) {
        console.error("Error fetching leaderboard:", error);
      }
    };

    fetchScores();
  }, []);
    const playersWithPositiveGold = leaderboard
    .filter(([playerName, gold]) => gold > 0) // Keep only players with gold > 0
    .map(([playerName]) => playerName); // Extract just the names
    // Filter playerNames to exclude the currentPlayer
    useEffect(() => {
        if (leaderboard.length > 0) {
            // Filter playerNames based on the leaderboard data
            const playersWithPositiveGold = leaderboard
                .filter(([playerName, gold]) => gold > 0) // Keep only players with gold > 0
                .map(([playerName]) => playerName); // Extract just the names

            const filteredPlayers = playerNames.filter(
                (name, index) =>
                    index !== currentPlayerIndex && playersWithPositiveGold.includes(name)
            );

            setOtherPlayers(filteredPlayers); // Update the filtered players
        }
    }, [leaderboard, playerNames, currentPlayerIndex]);
   

    const handleDone = () => {
        navigate('/TurnTracking', { state: { 
            playerNames, 
            chestList,
            currentPlayerIndex : (currentPlayerIndex + 1) % playerNames.length, 
            nextTurn: true } });
    };

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

    return(
        <div>
            <div className = "banner">
                <a href="/Rules" target="_blank">Rule Book</a>
                {/* <a href="/StartGame">Game Log</a> */}
                <a href = "/NumberPlayer">Restart Game</a>
                <a href = "/" className = "quit">Quit</a>
            </div>
            <p>It's {playerNames[currentPlayerIndex]}'s turn! Let's play!</p>
            <div className='game-container'>
                <div className='game-button'>
                    <div><Excavation chestList={chestList} 
                             currentPlayer={currentPlayer}
                             currentPlayerIndex={currentPlayerIndex}
                             playerNames={playerNames}
                                     ></Excavation></div>
                    <div ><Attack attackPlayers={otherPlayers} 
                                playerNames={playerNames}
                                currentPlayer={currentPlayer}
                                currentPlayerIndex={currentPlayerIndex}/> </div>
                    <div><Trigger></Trigger></div>
                </div>
                <div className = "leaderboard">
                    <Leaderboard />
                </div>
                <button onClick={handleDone}>Done</button>
                <div>
                    <button onClick={() => handleGoldUpdate(100)}>Plus 100 Gold</button>
                    <button onClick={() => handleGoldUpdate(-100)}>Minus 100 Gold</button>
                </div>
            </div>
        </div>
    );
}

export default Game;
