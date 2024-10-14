from flask import Flask, jsonify
import DiceReading_CurrentLightFaces as dice_reader
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/trigger-dice", methods=['GET'])
def roll_dice():
    dice_roll = dice_reader.trigger_dice_reader()
    return jsonify({'dice_roll': dice_roll})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

