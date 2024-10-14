// Attack.js

import React from 'react';
import { useNavigate } from 'react-router-dom';

const Attack = ({ playerNames }) => {
    const navigate = useNavigate();

    const handleAttackClick = () => {
        navigate('/AttackSelection', { state: { playerNames } }); // Pass player names to the AttackSelection component
    };

    return (
        <div>
            <button onClick={handleAttackClick}>Attack!</button>
        </div>
    );
};

export default Attack;
