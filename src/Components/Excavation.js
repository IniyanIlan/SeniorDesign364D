import React from 'react';
import { useState } from 'react';


function Excavation(){
    const [prob, setProb] = useState('')
    const excavateButton = () => {
        var min = 1
        var max = 10
        var p = Math.random() * (max - min) + min //>= 1 and < 10
        if(p > 5){
            setProb('you found a bomb!')
        }
        else{
            setProb("you found treasure!")
        }
    }
    return(
        <div style={{display:'flex', flexDirection:'row'}}>
            <button classname="button" onClick={excavateButton}>Excavate!</button>
            <p>{prob}</p>
            
        </div>
    );
};

export default Excavation