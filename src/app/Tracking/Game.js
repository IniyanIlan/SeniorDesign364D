import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Leaderboard from './Leaderboard';
import Excavation from '../Action/Excavation';
import Trigger from '../Action/TriggerDice';
import './Game.css';
import Attack from '../Action/Attack';


const Game = () => {
    const { state } = useLocation();
    const { playerNames, chestList } = state;
    return(
        <div>
            <div className = "banner">
                <a href="/Rules" target="_blank">Rule Book</a>
                <a href="/StartGame">Game Log</a>
                <a href = "/NumberPlayer">Restart Game</a>
                <a href = "/" className = "quit">Quit</a>
            </div>
            
            <div className = "game-container">
                <div>
                <Excavation chestList={chestList}></Excavation>
                </div>
                <div>
                <Attack /> 
                </div>
                <div className = "game-button">
                    <Trigger></Trigger>
                </div>
                
                <div className = "leaderboard">
                    <Leaderboard playerNames={state.playerNames}/>
                </div>
            </div>
        </div>
    );
}

export default Game;