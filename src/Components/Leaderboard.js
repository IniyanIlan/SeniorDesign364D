import React from 'react';
import '../CSS/Leaderboard.css';

const Leaderboard = () => {
  return (
    <div className = "flex-container">
      <board>
        <div>
          <row>Rank</row>
          <row>Name</row>
          <row>Score</row>
        </div>
      </board>
    </div>
    
  );
}  

export default Leaderboard;