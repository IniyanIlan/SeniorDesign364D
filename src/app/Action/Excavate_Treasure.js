import React from 'react';
import { useState } from 'react';
import { useNavigate } from "react-router";

const Excavate_Treasure = () => {

    return(
        <div>
            <h1>you found treasure!</h1>
            <a href = "/Game" className = "quit">Quit</a>
        </div>
    )
}

export default Excavate_Treasure;