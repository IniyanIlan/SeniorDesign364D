from flask import Flask, jsonify
from flask_cors import CORS
from multiprocessing.resource_tracker import unregister
from multiprocessing import shared_memory
from picamera2 import Picamera2, Preview
import numpy as np
import time
import subprocess
import action
import sys

app = Flask(__name__)
CORS(app)  

diceRequest = None
diceData = None
shmRequest = None
shmDiceData = None

@app.route("/")
def home():
    action.initialize_chests()
    print(action.chest_list)
    return jsonify({"message": "Chests initialized", "chests": action.chest_list})

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

# @app.route("/trigger-dice", methods=['GET'])
# def roll_dice():
#    dice_roll = dice_reader.trigger_dice_reader()
#    print("From API=======================================")
#    print(dice_roll)
#    print("=======================================")
#    return jsonify({'dice_roll': dice_roll})


def gameBoard_Init():
    tempdiceRequest = np.array([0], dtype=np.int8)
    tempdiceData = np.array([-1], dtype=np.int8)
    shmRequest = shared_memory.SharedMemory(create=True, size=tempdiceRequest.nbytes)
    shmDiceData = shared_memory.SharedMemory(create=True, size=tempdiceData.nbytes)
    diceRequest = np.ndarray(tempdiceRequest.shape, dtype=tempdiceRequest.dtype, buffer=shmRequest.buf)
    diceData = np.ndarray(tempdiceData.shape, dtype=tempdiceData.dtype, buffer=shmDiceData.buf)
    diceRequest[:] = tempdiceRequest[:]
    diceData[:] = tempdiceData[:]
    
    

if __name__ == '__main__':
    gameBoard_Init()
    process = subprocess.Popen(['python3', 'DiceReading_CurrentLightFaces.py', shmRequest.name, shmDiceData.name])
    app.run(debug=True, port=5000)
    
    
