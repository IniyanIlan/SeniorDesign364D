import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Leaderboard from './Leaderboard';
import Excavation from '../Action/Excavation';
import Trigger from '../Action/TriggerDice';
import './Game.css';
import Attack from '../Action/Attack';


const Game = () => {
    const { state } = useLocation();
    const navigate = useNavigate();
    const { playerNames, currentPlayerIndex, chestList } = state;

    const handleDone = () => {
        navigate('/TurnTracking', { state: { 
            playerNames, 
            chestList,
            currentPlayerIndex : (currentPlayerIndex + 1) % playerNames.length, 
            nextTurn: true } });
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
                    <div><Excavation chestList={chestList}></Excavation></div>
                    <div ><Attack /> </div>
                    <div><Trigger></Trigger></div>
                </div>
                <div className = "leaderboard">
                    <Leaderboard playerNames={playerNames}/>
                </div>
                <button onClick={handleDone}>Done</button>
            </div>
        </div>
    );
}

export default Game;