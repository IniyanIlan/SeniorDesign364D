from flask import Flask, jsonify
from flask_cors import CORS
import action


app = Flask(__name__)
CORS(app)  

@app.route("/")
def home():
    action.initialize_chests()
    return jsonify({"message": "Chests initialized", "chests": action.chest_list})

@app.route("/excavate")
def try_excavate():
    print(f"Chest list before excavation: {action.chest_list}")
    result = action.excavate()
    if result == -1:
        return jsonify({"message": "No more chests to excavate!"}), 400
    return jsonify({"result": result})

@app.route("/attack")
def try_attack():
    result = action.attack()
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
