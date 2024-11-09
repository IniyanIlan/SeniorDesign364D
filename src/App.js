import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './app/SettingUp/Home';
import PlayerNameEntry from './app/SettingUp/PlayerNameEntry';
import Game from './app/Tracking/Game';
import Rules from './app/SettingUp/Rules';
import NumberPlayer from './app/SettingUp/NumberPlayer';
import './App.css';
import Excavate_Bomb from './app/Action/Excavate_Bomb';
import Excavate_Treasure from './app/Action/Excavate_Treasure';
import Attack from './app/Action/Attack';
import TurnTracking from './app/Tracking/TurnTracking';
import Winner from './app/Tracking/Winner';
import Attack_Selection from './app/Action/Attack_Selection';

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
          <Route path="/Excavate_Bomb" element={<Excavate_Bomb/>}> </Route>
          <Route path="/Excavate_Treasure" element={<Excavate_Treasure/>}></Route>
          <Route path="/Attack" element={<Attack />} />
          <Route path="/TurnTracking" element={<TurnTracking />}/>
          <Route path="/Winner" element={<Winner />}/>
          <Route path="/Attack_Selection" element={<Attack_Selection />}/>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
