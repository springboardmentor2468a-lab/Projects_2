from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import random

app = Flask(__name__)

# Load trained models
hour_model = pickle.load(open("models/hour_model.pkl", "rb"))
day_model = pickle.load(open("models/day_model.pkl", "rb"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    mode = data["mode"]

    temp = float(data["temp"])
    humidity = float(data["humidity"])
    wind = float(data["wind"])
    event = int(data["event"])

    base_features = np.array([[temp, humidity, wind, event]])

    predictions = []

    

    if mode == "hour":
        base = max(0, int(hour_model.predict(base_features)[0]))
        for i in range(6):
            val = base + random.randint(-20, 20)
            predictions.append(max(0, val))  
    else:
        base = max(0, int(day_model.predict(base_features)[0]))
        for i in range(6):
            val = base + random.randint(-200, 200)
            predictions.append(max(0, val))   

    return jsonify({
        "mode": mode,
        "values": predictions
    })

if __name__ == "__main__":
    app.run(debug=True)
