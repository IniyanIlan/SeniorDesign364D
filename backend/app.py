from flask import Flask, jsonify, request
from flask_cors import CORS
from multiprocessing.resource_tracker import unregister
from multiprocessing import shared_memory
import numpy as np
import time
import subprocess
import action
import sys
import os

app = Flask(__name__)
CORS(app)  

# Initialize a global dictionary for leaderboard
leaderboard_dict = {}
winning_gold = 500
color_indices = []

# Shared Memory Stuff Starts Here

try:
    # Try to connect to an existing shared memory block
    existing_shm = shared_memory.SharedMemory(name='DiceData')
    existing_shm.unlink()  # Unlink the existing shared memory block
    existing_shm.close()   # Close the existing shared memory block
except FileNotFoundError:
    # If not found, it means no shared memory block by that name exists
    pass

try:
    # Try to connect to an existing shared memory block
    existing_shm = shared_memory.SharedMemory(name='PresentMatrix')
    existing_shm.unlink()  # Unlink the existing shared memory block
    existing_shm.close()   # Close the existing shared memory block
except FileNotFoundError:
    # If not found, it means no shared memory block by that name exists
    pass

try:
    # Try to connect to an existing shared memory block
    existing_shm = shared_memory.SharedMemory(name='PastMatrix')
    existing_shm.unlink()  # Unlink the existing shared memory block
    existing_shm.close()   # Close the existing shared memory block
except FileNotFoundError:
    # If not found, it means no shared memory block by that name exists
    pass

try:
    # Try to connect to an existing shared memory block
    existing_shm = shared_memory.SharedMemory(name='MatrixRequest')
    existing_shm.unlink()  # Unlink the existing shared memory block
    existing_shm.close()   # Close the existing shared memory block
except FileNotFoundError:
    # If not found, it means no shared memory block by that name exists
    pass

try:
    # Try to connect to an existing shared memory block
    existing_shm = shared_memory.SharedMemory(name='MatrixDataReady')
    existing_shm.unlink()  # Unlink the existing shared memory block
    existing_shm.close()   # Close the existing shared memory block
except FileNotFoundError:
    # If not found, it means no shared memory block by that name exists
    pass

try:
    # Try to connect to an existing shared memory block
    existing_shm = shared_memory.SharedMemory(name='DiceRequest')
    existing_shm.unlink()  # Unlink the existing shared memory block
    existing_shm.close()   # Close the existing shared memory block
except FileNotFoundError:
    pass

try:
    # Try to connect to an existing shared memory block
    existing_shm = shared_memory.SharedMemory(name='DiceShutdown')
    existing_shm.unlink()  # Unlink the existing shared memory block
    existing_shm.close()   # Close the existing shared memory block
except FileNotFoundError:
    pass

try:
    existing_shm = shared_memory.SharedMemory(name='LEDRequest')
    existing_shm.unlink()
    existing_shm.close()
except FileNotFoundError:
    pass


tempdiceRequest = np.array([0], dtype=np.int8)
tempdiceData = np.array([-1], dtype=np.int8)
tempShutdown = np.array([0], dtype=np.int8)
shmRequest = shared_memory.SharedMemory(create=True, size=tempdiceRequest.nbytes, name='DiceRequest')
shmDiceData = shared_memory.SharedMemory(create=True, size=tempdiceData.nbytes, name='DiceData')
shmShutdown = shared_memory.SharedMemory(create=True, size=tempShutdown.nbytes, name='DiceShutdown')
diceRequest = np.ndarray(tempdiceRequest.shape, dtype=tempdiceRequest.dtype, buffer=shmRequest.buf)
diceData = np.ndarray(tempdiceData.shape, dtype=tempdiceData.dtype, buffer=shmDiceData.buf)
shutdown = np.ndarray(tempdiceData.shape, dtype=tempShutdown.dtype, buffer=shmShutdown.buf)
shutdown[:] = tempShutdown[:]
diceRequest[:] = tempdiceRequest[:]
diceData[:] = tempdiceData[:]

# Index 0 = Mode of LED {0 - Breathe, 1 - Waves, 2 - Explosion, 3 - Player, 4 - Off}, Index 1 = PlayerColor, Index 2 = LED Ready
tempLEDRequest = np.array([0, -1, 0], dtype= np.int16)
shmLEDRequest = shared_memory.SharedMemory(create=True, size=tempLEDRequest.nbytes, name='LEDRequest')
ledRequest = np.ndarray(tempLEDRequest.shape, dtype=tempLEDRequest.dtype, buffer=shmLEDRequest.buf)
ledRequest[:] = tempLEDRequest[:]


# Hall effect Matrix Init

#Define the shape and data type of the Present 2D array
array_shape = (5, 8)  # For example, a 5x5 array
array_dtype = np.int8  # Specify the data type

# Array Size
nbytes = int(np.prod(array_shape) * np.dtype(array_dtype).itemsize)

# Create the shared memory block
shmMatrix = shared_memory.SharedMemory(create=True, size=nbytes, name='PresentMatrix')

# Create a 2D NumPy array backed by the shared memory
presentMatrix = np.ndarray(array_shape, dtype=array_dtype, buffer=shmMatrix.buf)

# Initialize the array with some values
presentMatrix[:] = 0
print(presentMatrix)


#Past Array Matrix Initialization

#Define the shape and data type of your 2D array
pastArraySshape = (5, 8)  # For example, a 5x5 array
array_dtype = np.int8  # Specify the data type

# Array Size
nbytes = int(np.prod(array_shape) * np.dtype(array_dtype).itemsize)

# Create the shared memory block
shmPastMatrix = shared_memory.SharedMemory(create=True, size=nbytes, name='PastMatrix')

# Create a 2D NumPy array backed by the shared memory
pastMatrix = np.ndarray(array_shape, dtype=array_dtype, buffer=shmMatrix.buf)



# Data Ready/Request Flags For Matrix
tempMatrixRequest = np.array([0, 0, 0], dtype=np.int64)
tempMatrixDataReady = np.array([0, 0, 0, 0, 0, 0], dtype=np.int64)
shmMatrixRequest = shared_memory.SharedMemory(create=True, size=tempMatrixRequest.nbytes, name='MatrixRequest')
shmMatrixDataReady = shared_memory.SharedMemory(create=True, size=tempMatrixDataReady.nbytes, name='MatrixDataReady')
matrixRequest = np.ndarray(tempMatrixRequest.shape, dtype=tempMatrixRequest.dtype, buffer=shmMatrixRequest.buf)
matrixDataReady = np.ndarray(tempMatrixDataReady.shape, dtype=tempMatrixDataReady.dtype, buffer=shmMatrixDataReady.buf)
# Use the values below.
matrixRequest[:] = tempMatrixRequest[:]
matrixDataReady[:] = tempMatrixDataReady[:]


@app.route("/")
def home():
    action.initialize_chests()
    print(action.chest_list)
    return jsonify({"message": "Chests initialized", "chests": action.chest_list})

@app.route("/chest_locations", methods=["GET"])
def chest_locations():
    chest_locations = action.get_locations()
    print(chest_locations)
    return jsonify({"chest_locations": chest_locations})

@app.route("/init_leaderboard", methods=["POST"])
def init_leaderboard():
    data = request.json
    player_names = data.get("playerNames", [])
    # Initialize each player's score to 0
    global color_indices
    global leaderboard_dict
    leaderboard_dict = {name: 0 for name in player_names}
    color_indices = data.get("colorIndices", [])
    for i in color_indices:
        matrixDataReady[0] = i
        matrixRequest[0] = 4
        timeout = time.time() + 5
        while(matrixRequest[0] != 0 and time.time() < timeout):
            pass
    print(f"Leaderboard initialized: {leaderboard_dict}")
    return jsonify({"message": "Leaderboard initialized", "leaderboard": leaderboard_dict})

@app.route("/update_gold", methods=["POST"])
def update_gold():
    data = request.json
    player_name = data.get("playerName")
    gold_change = data.get("goldChange", 0)
    
    if player_name in leaderboard_dict:
        leaderboard_dict[player_name] += gold_change
        print(f"{player_name}'s score updated, new_score: {leaderboard_dict[player_name]}")
        print(f"Leaderboard Updated: {leaderboard_dict}")
        return jsonify({"message": f"{player_name}'s score updated", "new_score": leaderboard_dict[player_name]})
    else:
        return jsonify({"message": "Player not found"}), 404

@app.route("/get_leaderboard", methods=["GET"])
def get_leaderboard():
    sorted_leaderboard = sorted(leaderboard_dict.items(), key=lambda item: item[1], reverse=True)
    print(f"Sorted Leaderboard: {sorted_leaderboard}")
    return jsonify(sorted_leaderboard)

@app.route("/excavate")
def try_excavate():
    print(f"Chest list before excavation: {action.chest_list}")
    result = action.excavate()
    print(result)
    if result == -1:
        return jsonify({"message": "No more chests to excavate!"}), 400
    return jsonify({"result": result})

@app.route("/defusal")
def defusing():
    diceRequest[0] = 1
    timeout = time.time() + 10
    print("API waiting for result.....")
    while diceData[0] == -1:
        if time.time() > timeout:
            diceRequest[0] = 0
            print("Timeout")
            return jsonify({"message": "Timeout"}), 408
        pass
    dice_roll = diceData[0]
    print("+++++++++++++++++++++")
    print(f"We got a value: {dice_roll}")
    diceData[0] = -1
    return jsonify(value = int(dice_roll))

@app.route("/explosion_led", methods=["POST"])
def explosion():
    ledRequest[0] = 1

    return jsonify({"message": "Explosion triggered"})

@app.route("/player_led", methods=["POST"])
def player_led():
    data = request.json
    playerIndex = int(data.get("playerIndex", 0))
    print("Player "+ str(playerIndex) + " has color " + str(color_indices[playerIndex]))
    print(color_indices)
    #ledRequest[2] = 1
    #while ledRequest[2] != 0:
    ledRequest[0] = 2
    ledRequest[1] = color_indices[playerIndex]
    while(ledRequest[1] != color_indices[playerIndex]):
        ledRequest[1] = color_indices[playerIndex]
    ledRequest[2] = 1 # Ready
    return jsonify({"message": "Player LED triggered"})

@app.route("/get_chest_list")
def get_chest_list():
    return jsonify({"result": action.chest_list})

@app.route("/attack/<int:attackRoll>/<int:defenderRoll>", methods=["GET"])
def try_attack(attackRoll, defenderRoll):
    result = action.attack(attackRoll, defenderRoll)
    print(result)
    return jsonify({"result" : result})

# FOR TESTING WITHOUT PI
    # return jsonify({
    #         "result": 100
    #         })
    

    
# @app.route("/stop-picam", methods=['POST'])
# def stop_cam():
#     dice_reader.initialize_picam()
    # shmDiceData.close()
    # shmRequest.close()
    # shmShutdown.close()
    # shmDiceData.unlink()
    # shmRequest.unlink()
    # shmShutdown.unlink()
    #shmMatrix.close()
    #shmMatrix.unlink()

@app.route("/trigger-dice", methods=['GET'])
def trigger_dice():
    diceRequest[0] = 1
    timeout = time.time() + 25
    print("API waiting for result.....")
    while diceData[0] == -1:
        if time.time() > timeout:
            diceRequest[0] = 0
            print("Timeout")
            return jsonify({"message": "Timeout"}), 408
        pass
    dice_roll = diceData[0]
    print("+++++++++++++++++++++")
    print(f"We got a value: {dice_roll}")
    diceData[0] = -1
    return jsonify(value = int(dice_roll))

@app.route("/validate-move/<int:currentPlayerIndex>", methods=['GET'])
def validate_move(currentPlayerIndex):
    matrixRequest[0] = 1
    matrixRequest[1] = currentPlayerIndex + 1
    timeout = time.time() + 10
    while matrixDataReady[0] == 0:
        if time.time() > timeout:
            diceRequest[0] = 0
            print("Timeout")
            return jsonify({"message": "Timeout"}), 408
        pass
    
    x = matrixDataReady[2]
    y = matrixDataReady[3]


    if matrixDataReady[0] == 1:
        return jsonify({
            'valid' : True,
            'x_val' : x,
            'y_val' : y
        })
    elif matrixDataReady[0] == -1:
        return jsonify({
            'valid': False,
            'x_val' : x,
            'y_val' : y
        })



@app.route("/get_winner", methods=["GET"])
def get_winner():
    for player, score in leaderboard_dict.items():
        if score >= winning_gold:
            print(f"Winner found: {player} with score {score}")
            return jsonify({"winner": player})
    print("No winner yet.")
    return jsonify({"winner": None})

if __name__ == '__main__':
    print("Opening DiceReader file")
    
    app.run(debug=True, port=5001)
    
    
