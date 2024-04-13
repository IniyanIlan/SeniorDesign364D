// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';

// const TotalPLayer = ({ numberOfPlayers }) => {
//   const [playerNames, setPlayerNames] = useState(Array(numberOfPlayers).fill(''));
//   const navigate = useNavigate();

//   const handleInputChange = (index, event) => {
//     const newPlayerNames = [...playerNames];
//     newPlayerNames[index] = event.target.value;
//     setPlayerNames(newPlayerNames);
//   };

//   const handleSubmit = (event) => {
//     event.preventDefault();
//     navigate('/game', { state: { playerNames } });
//   };

//   return (
//     <div>
//       <h2>Enter Player Names</h2>
//       <form onSubmit={handleSubmit}>
//         {playerNames.map((playerName, index) => (
//           <div key={index}>
//             <label>Player {index + 1}:</label>
//             <input
//               type="text"
//               value={playerName}
//               onChange={(event) => handleInputChange(index, event)}
//               required
//             />
//           </div>
//         ))}
//         <button type="submit">Start Game</button>
//       </form>
//     </div>
//   );
// };

// const PlayerNameEntry = ({ onSubmit }) => {
//   const [numberOfPlayers, setNumberOfPlayers] = useState(5); // Default value is 5

//   const handleChange = (event) => {
//     setNumberOfPlayers(parseInt(event.target.value, 10)); // Convert input value to integer
//   };

//   const handleSubmit = (event) => {
//     event.preventDefault();
//     onSubmit(numberOfPlayers);
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       <label>
//         Number of Players:
//         <input
//           type="number"
//           value={numberOfPlayers}
//           onChange={handleChange}
//           min={1}
//           max={10} // Set maximum number of players if needed
//         />
//       </label>
//       <TotalPLayer numberOfPlayers="numberOfPlayers" />
//       <button type="submit">Submit</button>
//     </form>
//   );
// };

// export default PlayerNameEntry;










// PlayerNameEntry.js

import React, { useState } from 'react';
import {Link, useNavigate } from 'react-router-dom';

const PlayerNameEntry = ({ numberOfPlayers = 6 }) => {
  const [playerNames, setPlayerNames] = useState(Array(numberOfPlayers).fill(''));
  const navigate = useNavigate();

  const handleInputChange = (index, event) => {
    const newPlayerNames = [...playerNames];
    newPlayerNames[index] = event.target.value;
    setPlayerNames(newPlayerNames);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    <Link 
      to={{
        pathname: "/StartGame",
        state: {playerNames} 
      }}/>
    navigate('/StartGame', { state: { playerNames } });
  };

  return (
    <div>
      <h2>Enter Player Names</h2>
      <form onSubmit={handleSubmit}>
        {playerNames.map((playerName, index) => ( // Renamed 'name' to 'playerName'
          <div key={index}>
            <label>Player {index + 1}:</label>
            <input
              type="text"
              value={playerName} // Updated 'name' to 'playerName'
              onChange={(event) => handleInputChange(index, event)}
              required
            />
          </div>
        ))}
        <button type="submit">Start Game</button>
      </form>
    </div>
  );
};

export default PlayerNameEntry;
