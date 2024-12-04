import React, { useState } from 'react';
import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

const Initialization = () => {
    const location = useLocation();
    const { playerNames, selectedColors, chestList, chestLocations} = location.state || {};
    const [currentPlayerIndex, setCurrentPlayerIndex] = useState(0); // Track current player index
    const [locations, setLocations] = useState(chestLocations[0]);
    const navigate = useNavigate();

    const hexRadius = 50; // Radius of each hexagon
    const hexagons = [
    { x: 300, y: 100 },
    { x: 400, y: 100 },
    { x: 500, y: 100 },
    { x: 250, y: 200 },
    { x: 350, y: 200 },
    { x: 450, y: 200 },
    { x: 550, y: 200 },
    { x: 200, y: 300 },
    { x: 300, y: 300 },
    { x: 400, y: 300 },
    { x: 500, y: 300 },
    { x: 600, y: 300 },
    { x: 250, y: 400 },
    { x: 350, y: 400 },
    { x: 450, y: 400 },
    { x: 550, y: 400 },
    { x: 300, y: 500 },
    { x: 400, y: 500 },
    { x: 500, y: 500 },

    ];

    const playButtonSound = () => {
      const audio = new Audio('/click_3.mp3');
      audio.play();
      // playButtonSound();
    };

    const handleReady = () =>{
        playButtonSound();
        navigate('/TurnTracking', { state: { playerNames, selectedColors, chestList} });
    }

    useEffect(() => {
        if(chestLocations.length > 0){
            setLocations(chestLocations);
        }
        else{
            console.log("No chest locations");
        }

    },[chestLocations]);

    const getHexPoints = (cx, cy, r) => {
        const points = [];
        for (let i = 0; i < 6; i++) {
          const angle = (Math.PI / 3) * i; // 60-degree increments
          const x = cx + r * Math.sin(angle);
          const y = cy + r * Math.cos(angle);
          points.push(`${x},${y}`);
        }
        return points.join(" ");
    };
  
    return (
      <div>
        <div className = "banner">
                  <a href="/Rules" target="_blank">Rule Book</a>
                  {/* <a href="/StartGame">Game Log</a> */}
                  <a href = "/NumberPlayer">Restart Game</a>
                  <a href = "/" className = "quit">Quit</a>
        </div>
        <div className="game-columns">
            <div className = "welcome"> Before we get started... </div>
            <p>Place the chests in their proper spots as shown in the image</p>
            {/* <img
                className="board-image"
                src="/BoardGame.jpg" 
                alt="Board"
            /> */}
            <img
                className = "chest-img"
                src="/treasure-chest.jpg" 
                alt="Board"
            />
            <svg width="800" height="600" style={{ backgroundColor: "white" }}>
                {hexagons.map(({ x, y }, index) => (
                    <polygon
                    key={index}
                    points={getHexPoints(x, y, hexRadius)}
                    fill="lightblue"
                    stroke="#000"
                    strokeWidth="2"
                    
                    />
                ))}

                {chestLocations.map((amount, index) => {
                    const { x, y } = hexagons[index];
                    return Array.from({ length: amount }, (_, chestIndex) => (
                    <circle
                        key={`circle-${index}-${chestIndex}`}
                        cx={x + chestIndex * 10 - 10}
                        cy={y}
                        r="5"
                        fill="gold"
                    />
                    ));
                })}
                </svg>
            {/* <div>
                {
                        chestLocations.map((amount, index) => (
                            <p key={index}>Place {amount} chests on tile {index+1}</p>
                        ))
                }
            </div> */}
            <button className="button" onClick={handleReady}>Ready!</button>
          {/* <Trigger></Trigger> */}
        </div>
      </div>
      
    );
  };

export default Initialization;
