
# 🚲 RideWise – Bike Sharing Demand Prediction System

## 📌 Project Overview

**RideWise** is a full-stack machine learning application designed to **predict bike-sharing demand** based on **weather conditions, time-based features, and urban factors**.
The system helps city planners and bike rental companies optimize fleet availability and resource allocation.

This project uses:

* **Machine Learning model trained in Google Colab**
* **Flask REST API backend (Python)**
* **React.js frontend**
* **Pickle (`.pkl`) model integration**

---

## 🧠 Machine Learning Model

* The ML model is trained in **Google Colab**
* Dataset sourced from Kaggle Bike Sharing Dataset
* Regression techniques are used to predict **hourly bike rental count**
* The trained model is exported as a **Pickle file (`.pkl`)**
* This Pickle file is downloaded and integrated into the Flask backend for inference

### Model Input Features (Example)

* Hour
* Temperature
* Humidity
* Weather condition
* Working day / holiday
* Season

### Output

* **Predicted bike rental count**

---

## 🏗️ System Architecture

```
React Frontend
     |
     | (HTTP Requests - JSON)
     v
Flask Backend (app.py)
     |
     | Loads trained model (.pkl)
     v
Machine Learning Model
```

---

## 🖥️ Tech Stack

### Frontend

* React.js
* JavaScript
* HTML5 / CSS3
* Axios (for API calls)
* Node.js & npm

### Backend

* Python
* Flask
* Flask-CORS
* NumPy
* Pandas
* Scikit-learn
* Pickle

### ML Development

* Google Colab
* Kaggle Dataset
* Scikit-learn

---

## 📂 Project Structure

```
RideWise/
│
├── backend/
│   ├── app.py
│   ├── model.pkl
│   ├── requirements.txt
│
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   ├── index.js
│
├── README.md
```

---

## ⚙️ Backend Setup (Flask API)

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Sample `requirements.txt`

```
flask
flask-cors
numpy
pandas
scikit-learn
```

### 3️⃣ `app.py` (Main Flask App)

```python
from flask import Flask, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load trained model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    features = np.array([data["features"]])
    prediction = model.predict(features)
    return jsonify({"prediction": int(prediction[0])})

if __name__ == "__main__":
    app.run(debug=True)
```

### 4️⃣ Run Backend Server

```bash
python app.py
```

Backend will run at:

```
http://127.0.0.1:5000
```

---

## ⚛️ Frontend Setup (React)

### 1️⃣ Install Node Modules

```bash
npm install
```

### 2️⃣ Run React App 

```bash
npm run dev
```

*(or `npm start` depending on setup)*

Frontend will run at:

```
http://localhost:3000
```

---

## 🔗 API Integration (React → Flask)

Example Axios call:

```javascript
axios.post("http://127.0.0.1:5000/predict", {
  features: [hour, temp, humidity, weather]
})
.then(response => {
  console.log(response.data.prediction);
});
```

---

## 📊 Key Features

* Real-time bike demand prediction
* Clean UI for user inputs
* Scalable backend architecture
* ML model abstraction using Pickle
* Easy deployment-ready structure

---

## 🎯 Use Cases

* Smart city transportation planning
* Bike fleet optimization
* Demand forecasting during events
* Weather-based resource planning

---

## 🧪 Model Evaluation Metrics

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)
* R² Score

---

## 🚀 Future Enhancements

* Deploy backend using Docker
* Cloud hosting (AWS / Render)
* Add authentication
* Advanced visualization dashboards
* Real-time weather API integration

---

## 👨‍💻 Author

**Dasari Varshith Narayana**


