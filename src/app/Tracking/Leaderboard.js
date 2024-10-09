import React from 'react';
import './Leaderboard.css';

function Leaderboard (props) {
  return (
    <div className = "leader-container">
        <h1>
          Leaderboard
        </h1>
        {props.playerNames.map((player, index) => {
          return (
            <div key={index}>
              <row>
                <column>{index + 1}</column>
                <column>{player}</column>
                <column>100</column>
              </row>
            </div>
          );
        })}
    </div>
    
  );
}  

export default Leaderboard;