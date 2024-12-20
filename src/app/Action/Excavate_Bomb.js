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
    const [attemptsLeft, setAttemptsLeft] = useState(5);
    const [numPips, setNumPips] = useState(0);
    const [playerLost, setPlayerLost] = useState(false);
    const [playerWon, setPlayerWon] = useState(false);

    const playButtonSound = () => {
        const audio = new Audio('/click_3.mp3');
        audio.play();
        // playButtonSound();
      };
 
    const playExplodeSound = () => {
        const audio = new Audio('/EXPLODE.wav');
        audio.play();
        // playExplodeSound();
      };
      
    const explodeLED = async () => {
        try{
            const res = await axios.post("http://localhost:5001/explosion_led");
            console.log("Explode LEDs have been activated" + res.data.message);
        }
        catch(error){
            console.error("Error activating LEDs:", error);
        }
    }

    const playGoldSound = () => {
        const audio = new Audio('/gold-louder.wav');
        audio.play();
        // playGoldSound();
    };
    const handleBackToGame = () => {
        playButtonSound();
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
        playButtonSound();
        console.log("Starting Dice Reader for defusual")
        try{
            const res = await axios.get("http://localhost:5001/defusal")
            setNumPips(res.data.value)
            console.log("Dice value:", res.data.value)
            if(res.data.value != randomNumber && attemptsLeft > 0){
                setAttemptsLeft(
                    (prevAttempt) => prevAttempt - 1)
            }
            else if(res.data.value == randomNumber){
                setPlayerWon(true)
                playGoldSound();
                handleGoldUpdate(150); 
            } 
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

    const handleLoss = async () =>{
        if(playerLost){
            handleGoldUpdate(-100)
        }
    }

    useEffect(() => {
        if(attemptsLeft == 0){
            playExplodeSound();
            explodeLED();
            setPlayerLost(true);
        }
    },[attemptsLeft]);

    useEffect(() =>{
        if(playerLost){
            handleGoldUpdate(-100)
        }
    }, [playerLost])


    return(
        <div className='center-container'>
            <div className='centered-content'>
                <h1 className='title'>You Found a Trapped Chest!</h1>
                <div>
                    Roll {randomNumber} to defuse! 
                    Attempts Remaining: {attemptsLeft}
                    {playerLost &&  <p>You failed to disengage the trap! -100 gold</p>}
                    {playerWon && <p>You defused the trap! +150 gold</p>}
                    <button className = "button" disabled={playerWon || attemptsLeft<=0} onClick={handleAttempt}>Attempt Defuse</button>
                </div>
                <button className = "button" disabled={attemptsLeft>0 && !playerWon} onClick={handleBackToGame}>Back to Game</button>
            </div>
        </div>
    )
}

export default Excavate_Bomb;