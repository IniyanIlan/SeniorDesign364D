from flask import Flask
import action

app = Flask(__name__)

@app.route("/")
def home():
    action.initialize_chests()
    return f"Hello, Flask! {action.chest_list}"

@app.route("/excavate")
def try_excavate():
    print(f"Chest list before excavation: {action.chest_list}")
    result = action.excavate()
    print(f"Chest list after excavation: {action.chest_list}")
    print(f"Excavate result: {result}")
    return f"Result: {result}"

if __name__ == '__main__':
    app.run(debug=True)
