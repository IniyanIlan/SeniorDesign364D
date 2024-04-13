import React from 'react';
import '../CSS/Leaderboard.css';

function Leaderboard (props) {
  return (
    <div className = "flex-container">
      <board>
        <rh>
          <rowh>Rank</rowh>
          <rowh>Name</rowh>
          <rowh>Score</rowh>
        </rh>
        {props.playerNames.map((player, index) => {
          return (
            <div key={index}>
              <row>{index + 1}</row>
              <row>{player}</row>
              <row>{player.score}</row>
            </div>
          );
        })}
      </board>
    </div>
    
  );
}  

export default Leaderboard;