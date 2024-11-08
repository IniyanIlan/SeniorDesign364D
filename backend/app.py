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

tempdiceRequest = np.array([0], dtype=np.int8)
tempdiceData = np.array([-1], dtype=np.int8)
tempShutdown = np.array([0], dtype=np.int8)
shmRequest = shared_memory.SharedMemory(create=True, size=tempdiceRequest.nbytes)
shmDiceData = shared_memory.SharedMemory(create=True, size=tempdiceData.nbytes)
shmShutdown = shared_memory.SharedMemory(create=True, size=tempShutdown.nbytes)
diceRequest = np.ndarray(tempdiceRequest.shape, dtype=tempdiceRequest.dtype, buffer=shmRequest.buf)
diceData = np.ndarray(tempdiceData.shape, dtype=tempdiceData.dtype, buffer=shmDiceData.buf)
shutdown = np.ndarray(tempdiceData.shape, dtype=tempShutdown.dtype, buffer=shmShutdown.buf)
shutdown[:] = tempShutdown[:]
diceRequest[:] = tempdiceRequest[:]
diceData[:] = tempdiceData[:]

# Hall effect Matrix Init

# Define the shape and data type of your 2D array
array_shape = (5, 8)  # For example, a 5x5 array
array_dtype = np.int8  # Specify the data type

# Array Size
nbytes = np.prod(array_shape) * np.dtype(array_dtype).itemsize

# Create the shared memory block
shmMatrix = shared_memory.SharedMemory(create=True, size=nbytes)

# Create a 2D NumPy array backed by the shared memory
shared_array = np.ndarray(array_shape, dtype=array_dtype, buffer=shmMatrix.buf)

# Initialize the array with some values
shared_array[:] = np.arange(np.prod(array_shape)).reshape(array_shape)

print(shared_array)

@app.route("/")
def home():
    action.initialize_chests()
    print(action.chest_list)
    return jsonify({"message": "Chests initialized", "chests": action.chest_list})

@app.route("/init_leaderboard", methods=["POST"])
def init_leaderboard():
    data = request.json
    player_names = data.get("playerNames", [])
    
    # Initialize each player's score to 0
    global leaderboard_dict
    leaderboard_dict = {name: 0 for name in player_names}
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

@app.route("/get_chest_list")
def get_chest_list():
    return jsonify({"result": action.chest_list})

@app.route("/attack")
def try_attack():
    result = action.attack()
    return jsonify({"result": result})
    
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
    print("API waiting for result.....")
    while diceData[0] == -1:
        x = 1
    dice_roll = diceData[0]
    print("+++++++++++++++++++++")
    print(f"We got a value: {dice_roll}")
    diceData[0] = -1
    return jsonify(value = int(dice_roll))

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
    
    file = open("shm_file.txt", "w")
    file.truncate()
    file.write(shmRequest.name + "\n")
    file.write(shmDiceData.name+ "\n")
    file.write(shmShutdown.name+ "\n")
    
    file.close()

    # process = subprocess.Popen(['python3', '../backend/DiceReading_CurrentLightFaces.py', 
    #                             shmRequest.name, shmDiceData.name, shmShutdown.name],preexec_fn=os.setpgrp)
    
    app.run(debug=True, port=5001)
    
    
