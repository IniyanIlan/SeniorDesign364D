import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Leaderboard from '../Components/Leaderboard';

const Game = () => {
    const { state } = useLocation();
    return(
        <>
        <div>
            <h1>Game Page</h1>
            <p>Player Names: {state.playerNames.join(', ')}</p>
        </div>
        </>
    );
}

export default Game;