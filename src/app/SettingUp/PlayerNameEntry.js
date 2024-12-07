import React, { useState } from 'react';
import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

const PlayerNameEntry = () => {
  const location = useLocation();
  const { numberOfPlayers, chestList } = location.state || {};
  const [playerNames, setPlayerNames] = useState(Array(numberOfPlayers).fill(''));
  const [selectedColors, setSelectedColors] = useState(Array(numberOfPlayers).fill(''));
  const [availableColors] = useState(['Red','Orange', 'Blue', 'Purple','Gold', 'Pink']); // Define initial colors
  const [chestLocations, setLocations] = useState([]);
  const navigate = useNavigate();

  const playButtonSound = () => {
    const audio = new Audio('/click_3.mp3');
    audio.play();
  };

  useEffect(() => {
    const fetchChestLocations = async () => {
      try {
        const res = await axios.get("http://localhost:5001/chest_locations");
        console.log(res.data.chest_locations);
        setLocations(res.data.chest_locations);
      } 
      catch (error) {
        console.error("Error fetching chest locations:", error);
      }
    };
    fetchChestLocations();
  },[])

  const handleInputChange = (index, event) => {
    const newPlayerNames = [...playerNames];
    newPlayerNames[index] = event.target.value;
    setPlayerNames(newPlayerNames);
  };

  const handleColorChange = (index, event) => {
    const newColor = event.target.value;

    // Update selectedColors with the new color
    const newSelectedColors = [...selectedColors];
    newSelectedColors[index] = newColor;
    setSelectedColors(newSelectedColors);
  };

  const getAvailableColors = (index) => {
    // Exclude colors already selected by other players
    return availableColors.filter(
      (color) => !selectedColors.includes(color) || selectedColors[index] === color
    );
  };

  const handleSubmit = async (event) => {
    playButtonSound();
    event.preventDefault();

    // Validate if all colors are selected
    if (selectedColors.some((color) => color === '')) {
      alert('Please select a color for every player.');
      return;
    }

    const colorIndices = selectedColors.map((color) => availableColors.indexOf(color));
    console.log("color indices: ", colorIndices)

    try {
      await axios.post("http://localhost:5001/init_leaderboard", { playerNames, colorIndices});
      navigate('/Initialization', { 
        state: { 
          playerNames,
          selectedColors,
          chestList,
          chestLocations
        }
      });
    } catch (error) {
      console.error("Error initializing players on backend:", error);
    }
  };

  return (
    <div className="container">
      <h2 className="title">Enter Player Names and Colors</h2>
      <form onSubmit={handleSubmit}>
        {playerNames.map((playerName, index) => (
          <div key={index} style={{ marginBottom: '1em' }}>
            <label>Player {index + 1}:</label>
            <input
              type="text"
              value={playerName}
              onChange={(event) => handleInputChange(index, event)}
              required
              style={{ marginRight: '1em' }}
            />
            <select
              value={selectedColors[index]}
              onChange={(event) => handleColorChange(index, event)}
              required
            >
              <option value="" disabled>
                Select Color
              </option>
              {getAvailableColors(index).map((color) => (
                <option key={color} value={color}>
                  {color}
                </option>
              ))}
            </select>
          </div>
        ))}
        <button className="button" type="submit">Start Game</button>
      </form>
      <h2>Place your piece on the corresponding colored dot!</h2>
    </div>
  );
};

export default PlayerNameEntry;
