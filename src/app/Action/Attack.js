

import React, { useState } from 'react';

const Attack = () => {
    const [message, setMessage] = useState(""); // State to store the attack message

    const handleAttackClick = async () => {
        try {
            const response = await fetch("http://localhost:5001/attack"); // Call the backend API
            const data = await response.json(); // Parse the JSON response
            
            if (response.ok) {
                // Check the result and set the message accordingly
                if (data.result === 0) {
                    setMessage(`You attacked and won!`);
                } else {
                    setMessage(`You attacked and lost!`);
                }
            } else {
                setMessage("Attack failed.");
            }
        } catch (error) {
            console.error("Error during attack:", error);
            setMessage("An error occurred.");
        }
    };

    return (
        <div>
           <button className='button' onClick={handleAttackClick}>Attack!</button>
           {message && <p>{message}</p>}
        </div>
    );
};

export default Attack;
