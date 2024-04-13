import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './page/Home';
import PlayerNameEntry from './page/PlayerNameEntry';
import Game from './page/Game';
import './App.css';



function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/PlayerEnterName" element={<PlayerNameEntry />} />
          <Route path="/StartGame" element={<Game />}/>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
