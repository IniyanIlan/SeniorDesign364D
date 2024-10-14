import React from 'react';
import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from "react-router";

function Excavation(){
    const navigate = useNavigate();
    const [result, setResult] = useState('');
    const excavateButton = async () => {
        try {
            const response = await axios.post('http://localhost:3000/excavate', {
            });
            setResult(response.data.result);  // Set result to state
          } catch (error) {
            console.error('There was an error!', error);
          }
        if(result === 0){
            /*found treasure */
            navigate('/Excavate_Treasure')
        }
        else{
            /*found bomb */
            navigate('/Excavate_Bomb')
        }
    }
    return(
        <div style={{display:'flex', flexDirection:'row'}}>
            <button classname="button" onClick={excavateButton}>Excavate!</button>
        </div>
    );
};

export default Excavation