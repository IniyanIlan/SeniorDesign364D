import React from 'react';
import './Leaderboard.css';

function Leaderboard (props) {
  return (
    <div className = "board-container">
        <h1>
          Leaderboard
        </h1>
        <div className = "stats">
          {props.playerNames.map((player, index) => {
            return (
              <div className="row" key={index}>
                <span className="column">{index + 1}.</span>
                <span className="column player-name">{player}</span>
                <span className="column player-score">100</span>
            </div>
            );
          })}
        </div>
        
    </div>
    
  );
}  

export default Leaderboard;