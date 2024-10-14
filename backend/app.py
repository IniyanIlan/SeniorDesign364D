from flask import Flask, jsonify
from flask_cors import CORS
import DiceReading_CurrentLightFaces as dice_reader

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/trigger-dice", methods=['GET'])
def roll_dice():
    dice_roll = dice_reader.trigger_dice_reader()
    return jsonify({'dice_roll': dice_roll})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)

