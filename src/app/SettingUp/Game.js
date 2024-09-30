import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Leaderboard from '../Tracking/Leaderboard';
import Excavation from '../Action/Excavation';

const Game = () => {
    const { state } = useLocation();
    return(
        <>
        <div>
            <h1 style={
                {textAlign: 'center'}
            }>Game Page</h1>
            <Leaderboard playerNames={state.playerNames}/>
            <Excavation></Excavation>
        </div>
        </>
    );
}

export default Game;