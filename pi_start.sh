echo "Starting Tides of Treachery..."
cd ./src
npm start &
REACT_PID=$!

cd ../backend
source ./venv/bin/activate
python3 app.py &
FLASK_PID=$!

python3 DiceReading_CurrentLightFaces.py &
DICE_PID=$!

echo "Finishing script..."
