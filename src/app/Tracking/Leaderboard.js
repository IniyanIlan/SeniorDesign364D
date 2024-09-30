import React from 'react';
import './Leaderboard.css';

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
              <row>
                <column>{index + 1}</column>
                <column>{player}</column>
                <columnL>100</columnL>
              </row>
            </div>
          );
        })}
      </board>
    </div>
    
  );
}  

export default Leaderboard;