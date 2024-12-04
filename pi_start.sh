# handle_sigint(){
#     echo "Stopping the script..."n
#     kill -9 `lsof -i :3000`
#     kill -9 `lsof -i :5001`
#     exit 0
# }

# trap handle_sigint SIGINT

echo "Starting Tides of Treachery..."
cd ./src
npm start &
REACT_PID=$!

cd ../backend
source ./venv/bin/activate
python3 app.py &
FLASK_PID=$!

#python3 DiceReading_CurrentLightFaces.py &
#DICE_PID=$!

python3 GameBoardMatrix.py &
BOARD_PID=$!

python3 Neopixel.py &
NEO_PID=$!

echo "Finishing script..."

cleanup() {
  echo "Stopping all processes..."
  kill $REACT_PID
  kill $FLASK_PID
  #kill $DICE_PID
  kill $BOARD_PID
  kill $NEO_PID
  echo "All processes stopped."
}

# Catch signals to stop processes on exit
trap cleanup SIGINT

wait
