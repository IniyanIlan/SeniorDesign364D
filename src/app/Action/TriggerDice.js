import React from 'react';
import { useState } from 'react';
import axios from 'axios';


function Trigger(){


    const [numPips, setNumPips] = useState(0)

    const handleTrigger = async () => {
        console.log("Starting Dice Reader")
        try{
            const res = await axios.get("http://localhost:5000/trigger-dice")
            setNumPips(res.data.dice_roll)
            console.log("Dice value:", res.data.dice_roll)
        }
        catch(error){
            console.error('Error fetching dice value:', error);
            setNumPips(0)
        }
    }

    return (
        <div>
            <button onClick={handleTrigger}>
                Trigger Dice
            </button>
            {numPips !== null && <h2>Dice Value: {numPips}</h2>}
        </div>
    );
}

export default Trigger;