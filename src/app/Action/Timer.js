import React, { useState, useEffect } from 'react';

function Timer() {
  const [timeLeft, setTimeLeft] = useState(10);  // Set the initial time (in seconds)
  const [attemptsLeft, setAttemptsLeft] = useState(5)

  useEffect(() => {
    // If the timer reaches zero, stop the interval
    if (timeLeft === 0) return;

    const timerId = setInterval(() => {
      setTimeLeft(prevTime => prevTime - 1);  // Decrease the time by 1 second
    }, 1000);  // 1000ms = 1 second

    // Cleanup the interval when the component is unmounted or the timer stops
    return () => clearInterval(timerId);
  }, [timeLeft]);



  
  return (
    <div>
      <h1>Attempts Remaining: {attemptsLeft}
        <button className='button'></button>
      </h1>
    </div>
  );
}

export default Timer;