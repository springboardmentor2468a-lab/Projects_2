from flask import Flask, request, jsonify, send_from_directory
import joblib
import numpy as np
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

hour_model = joblib.load(os.path.join(BASE_DIR, "hour_model.pkl"))
day_model  = joblib.load(os.path.join(BASE_DIR, "day_model.pkl"))

print("Hour model expects:", hour_model.n_features_in_)
print("Day model expects:", day_model.n_features_in_)

@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    mode = data["mode"]
    base_features = list(map(float, data["features"]))

    model = hour_model if mode == "hour" else day_model
    required = model.n_features_in_

    predictions = []

    for step in range(1, 7):  # next 6 steps
        features = base_features.copy()

        # 👉 shift time feature
        if mode == "hour":
            features[-3] = (features[-3] + step) % 24  # hour
        else:
            features[-3] = (features[-3] + step) % 7   # weekday

        # pad / trim
        if len(features) < required:
            features += [0.0] * (required - len(features))
        else:
            features = features[:required]

        X = np.array(features).reshape(1, -1)
        y = model.predict(X)[0]
        predictions.append(round(float(y), 2))

    return jsonify({
        "predictions": predictions
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
