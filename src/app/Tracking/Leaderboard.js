import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Leaderboard.css';

function Leaderboard () {
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    // Fetch player scores from the backend
    const fetchScores = async () => {
      try {
        const response = await axios.get("http://localhost:5001/get_leaderboard");
        setLeaderboard(response.data);
        console.log("Fetch sorted_leaderboard data:", response.data);
      } catch (error) {
        console.error("Error fetching leaderboard:", error);
      }
    };

    fetchScores();
  }, []);

  return (
    <div className="board-container">
      <h1>Leaderboard</h1>
      <div className="stats">
        {leaderboard.map(([player, score], index) => (
          <div className="row" key={index}>
            <span className="column player-name">{player}</span>
            <span className="column player-score">{score}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
//   return (
//     <div className = "board-container">
//         <h1>
//           Leaderboard
//         </h1>
//         <div className = "stats">
//           {/* {props.playerNames.map((player, index) => { */}

//             return (
//               <div className="row" key={index}>
//                 {/* <span className="column">{index + 1}.</span> */}
//                 <span className="column player-name">{player}</span>
//                 <span className="column player-score">0</span>
//             </div>
//             );
//           })}
//         </div>
        
//     </div>
    
//   );
// }  

export default Leaderboard;