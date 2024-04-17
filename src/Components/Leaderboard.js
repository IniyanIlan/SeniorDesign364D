import React from 'react';
import '../CSS/Leaderboard.css';

function Leaderboard (props) {
  return (
    <div className = "container">
      <board>
        <rh>
          <rowh>
            <column>Rank</column>
            <column>Player</column>
            <columnL>Gold</columnL>
          </rowh>
        </rh>
        {props.playerNames.map((player, index) => {
          return (
            <div key={index}>
              <row>
                <column>{index + 1}</column>
                <column>{player}</column>
                <columnL>{player.score}</columnL>
              </row>
            </div>
          );
        })}
      </board>
    </div>
    
  );
}  

export default Leaderboard;