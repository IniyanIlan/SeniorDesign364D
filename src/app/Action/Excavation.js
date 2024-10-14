import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Excavation = () => {
  const navigate = useNavigate();
  const [message, setMessage] = useState("");

  const handleExcavate = async () => {
    try {
      const response = await fetch("http://localhost:5000/excavate");
      const data = await response.json();

      if (response.ok) {
        if (data.result === 0) {
          navigate('/Excavate_Treasure');  // Navigate to the treasure component
        } else if (data.result === 1) {
          navigate('/Excavate_Bomb');  // Navigate to the bomb component
        }
      } else {
        setMessage(data.message);  // Display error message if no more chests
      }
    } catch (error) {
      console.error("Error excavating chest:", error);
      setMessage("An error occurred.");
    }
  };

  return (
    <div>
      <button onClick={handleExcavate}>Excavate</button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Excavation;
