from flask import Flask, jsonify
from flask_cors import CORS
#import DiceReading_CurrentLightFaces as dice_reader
import action

app = Flask(__name__)
CORS(app)  

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

# @app.route("/intialize-picam", methods=['GET'])
# def init_cam():
#     dice_reader.initialize_picam()
#     return jsonify({'message': 'Successfully turned on picam'})
    
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

if __name__ == '__main__':
    app.run(debug=True, port=5001)
