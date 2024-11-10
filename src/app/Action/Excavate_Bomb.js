import React from 'react';
import { useState, useEffect} from 'react';
import { useNavigate, useLocation } from "react-router";
import Timer from './Timer';
import Trigger from './TriggerDice'
import axios from 'axios';

const Excavate_Bomb = () => {
    const navigate = useNavigate();
    const { state } = useLocation();  // Get data passed from Excavation
    const playerNames = state.playerNames || [];
    const currentPlayer = state.currentPlayer;
    const currentPlayerIndex = state.currentPlayerIndex;
    const randomNumber = state.randomNumber;
    const [attemptsLeft, setAttemptsLeft] = useState(5) 
    const [numPips, setNumPips] = useState(0)
    const [playerLost, setPlayerLost] = useState(false);

    const handleBackToGame = () => {
        navigate('/TurnTracking', { state: { 
            playerNames, 
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


    const handleAttempt = async () => {
        console.log("Starting Dice Reader for defusual")
        try{
            const res = await axios.get("http://localhost:5001/defusal")
            setNumPips(res.data.value)
            console.log("Dice value:", res.data.value)
            setAttemptsLeft((prevAttempt) => prevAttempt - 1)
        }
        catch(error){
            if (error.code === 'ECONNABORTED' || error.response?.status === 408) {
                console.error("Timeout error: The request took too long to complete.");
            } 
            else{
                console.error("Error: unable to recieve dice request");
            }
            setNumPips(0);  // Set default or handle accordingly
            setAttemptsLeft((prevAttempt) => prevAttempt)
        }

    }

    useEffect(() => {
        if(attemptsLeft > 0){
            handleAttempt();
        }
        else{
            setPlayerLost(true)
            handleGoldUpdate(-100);
        }
    },[attemptsLeft, playerLost]);

    return(
        <div className='center-container'>
            <div className='centered-content'>
                <h1 className='title'>You Found a Bomb!</h1>
                <div>
                    Attempts Remaining: {attemptsLeft}
                    {playerLost &&  <p>You failed to disengage the trap! -100 gold</p>}
                </div>
                
                <button onClick={handleBackToGame}>Back to Game</button>
            </div>
        </div>
    )
}

export default Excavate_Bomb;