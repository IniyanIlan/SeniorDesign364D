import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './app/SettingUp/Home';
import PlayerNameEntry from './app/SettingUp/PlayerNameEntry';
import Game from './app/SettingUp/Game';
import Rules from './app/SettingUp/Rules';
import NumberPlayer from './app/SettingUp/NumberPlayer';
import './App.css';



function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/NumberPlayer" element={<NumberPlayer />} />
          <Route path="/PlayerEnterName" element={<PlayerNameEntry />} />
          <Route path="/StartGame" element={<Game />}/>
          <Route path="/Rules" element={<Rules />}/>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
