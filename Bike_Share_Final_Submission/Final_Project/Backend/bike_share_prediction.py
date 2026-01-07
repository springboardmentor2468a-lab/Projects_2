from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

# ---------------------------
# FILE PATHS (IMPORTANT)
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

day_csv_path = os.path.join(BASE_DIR, "day.csv")
hour_csv_path = os.path.join(BASE_DIR, "hour.csv")

# ---------------------------
# READ DATASETS
# ---------------------------
day_df = pd.read_csv(day_csv_path)
hour_df = pd.read_csv(hour_csv_path)

print("Datasets loaded successfully")

# ---------------------------
# ROUTES
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
