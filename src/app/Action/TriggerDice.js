import React from 'react';
import { useState } from 'react';
import { useNavigate, useLocation } from "react-router";
import axios from 'axios';


function Trigger(){

    const { state } = useLocation();
    const playerNames = state.playerNames || [];
    const currentPlayerIndex = state.currentPlayerIndex;
    const [numPips, setNumPips] = useState(0)

    const handleTrigger = async () => {
        console.log("Starting Dice Reader")
        try{
            const res = await axios.get("http://localhost:5001/trigger-dice")
            setNumPips(res.data.value)
            console.log("Dice value:", res.data.value)
        }
        catch(error){
            if (error.code === 'ECONNABORTED' || error.response?.status === 408) {
                console.error("Timeout error: The request took too long to complete.");
            } 
            else{
                console.error("Error: unable to recieve dice request");
            }
            setNumPips(0);  // Set default or handle accordingly
        }
        handleValidateMovement()
    }
    const handleValidateMovement = async () => {
        console.log("Validating Move")
        try{
            const res = await axios.get(`http://localhost:5001/validate-move/${currentPlayerIndex}`)
            const valid = res.data.valid
            if(valid){
                console.log("Player has made a valid move to ")
            }
        }
        catch(error){
            if (error.code === 'ECONNABORTED' || error.response?.status === 408) {
                console.error("Timeout error: The request took too long to complete.");
            } 
            else{
                console.error("Error: unable to validate move");
            }
            setNumPips(0);  // Set default or handle accordingly
        }
    }
    return (
        <div>
            <button className='button' onClick={handleTrigger}>
                Move
            </button>
            {numPips !== 0 && <h2>You rolled a {numPips}</h2>}
        </div>
    );
}

export default Trigger;