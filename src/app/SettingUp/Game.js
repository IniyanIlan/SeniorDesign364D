import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Leaderboard from '../Tracking/Leaderboard';
import Excavation from '../Action/Excavation';
import './Game.css';

const Game = () => {
    const { state } = useLocation();
    return(
        <div className = "game">
            <div className = "box">
                <a href="/Rules" target="_blank">Rule Book</a>
                <a href="/StartGame">Game Log</a>
                <a href = "/NumberPlayer">Restart Game</a>
                <a href = "/" class="push">Quit</a>
            </div>
            
            <Excavation></Excavation>
            <div className = "leaderboard">
                <Leaderboard playerNames={state.playerNames}/>
            </div>

        </div>
    );
}

export default Game;