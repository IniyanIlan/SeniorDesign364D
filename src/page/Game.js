import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Leaderboard from '../Components/Leaderboard';

const Game = () => {
    const { state } = useLocation();
    return(
        <>
        <div>
            <h1 style={
                {textAlign: 'center'}
            }>Game Page</h1>
            <Leaderboard playerNames={state.playerNames}/>
        </div>
        </>
    );
}

export default Game;