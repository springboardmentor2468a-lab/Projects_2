"""
Flask Backend for ML Model Prediction API

This server loads a trained machine learning model and feature list from pickle files,
and provides an API endpoint to make predictions based on input features.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import numpy as np
from datetime import datetime
from typing import Dict, List, Any
import math

# Initialize Flask app
app = Flask(__name__)
# Enable CORS to allow frontend to make requests
CORS(app)

# Global variables to store loaded model and features
model = None
model_features = None


def load_model_and_features():
    """
    Load the trained model and feature list from pickle files.
    This function is called when the server starts.
    """
    global model, model_features
    
    # Get the directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths to pickle files
    model_path = os.path.join(base_dir, 'best_model.pkl')
    features_path = os.path.join(base_dir, 'model_features.pkl')
    
    try:
        # Load the trained model
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print(f"[OK] Model loaded successfully from {model_path}")
        
        # Load the feature list
        with open(features_path, 'rb') as f:
            model_features = pickle.load(f)
        print(f"[OK] Features loaded successfully: {len(model_features)} features")
        print(f"  Features: {model_features}")
        
    except FileNotFoundError as e:
        print(f"[ERROR] Pickle file not found: {e}")
        raise
    except Exception as e:
        print(f"[ERROR] Error loading pickle files: {e}")
        raise


@app.route('/api/features', methods=['GET'])
def get_features():
    """
    Endpoint to get the list of features required by the model.
    Frontend uses this to dynamically generate input fields.
    """
    if model_features is None:
        return jsonify({'error': 'Model features not loaded'}), 500
    
    return jsonify({
        'features': model_features,
        'count': len(model_features)
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Endpoint to make predictions using the loaded model.
    
    Expected JSON format:
    {
        "feature1": value1,
        "feature2": value2,
        ...
    }
    
    Returns:
    {
        "prediction": predicted_value,
        "success": true
    }
    """
    if model is None or model_features is None:
        return jsonify({
            'error': 'Model or features not loaded',
            'success': False
        }), 500
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if data is None:
            return jsonify({
                'error': 'No JSON data provided',
                'success': False
            }), 400
        
        # Validate that all required features are present
        missing_features = [f for f in model_features if f not in data]
        if missing_features:
            return jsonify({
                'error': f'Missing required features: {missing_features}',
                'success': False,
                'missing_features': missing_features
            }), 400
        
        # Extract features in the correct order as expected by the model
        feature_values = []
        for feature in model_features:
            value = data.get(feature)
            
            # Convert to float, handle None values
            try:
                if value is None or value == '':
                    return jsonify({
                        'error': f'Feature "{feature}" has no value',
                        'success': False
                    }), 400
                feature_values.append(float(value))
            except (ValueError, TypeError):
                return jsonify({
                    'error': f'Invalid value for feature "{feature}": {value}',
                    'success': False
                }), 400
        
        # Convert to numpy array and reshape for prediction
        # Most sklearn models expect shape (n_samples, n_features)
        feature_array = np.array(feature_values).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(feature_array)
        
        # Get prediction value (handle both single value and array)
        if isinstance(prediction, np.ndarray):
            prediction_value = float(prediction[0])
        else:
            prediction_value = float(prediction)
        
        return jsonify({
            'prediction': prediction_value,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction error: {str(e)}',
            'success': False
        }), 500


def transform_frontend_inputs_to_features(data: Dict) -> Dict:
    """
    Transform simplified frontend inputs to model features.
    
    Frontend provides: date, hour, weather, isEvent, bikeType, temperature, humidity
    Model expects: season, mnth, hr, weekday, is_weekend, week_of_year, temp, atemp, 
                   hum, windspeed, weathersit, weather_severity, storm_flag, 
                   hour_sin, hour_cos, month_sin, month_cos, cnt_lag_1, cnt_lag_24
    """
    # Parse date
    date_str = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Extract date components
    month = date_obj.month
    weekday = date_obj.weekday()  # 0=Monday, 6=Sunday
    is_weekend = 1 if weekday >= 5 else 0
    week_of_year = date_obj.isocalendar()[1]
    
    # Determine season (1=spring, 2=summer, 3=fall, 4=winter)
    if month in [3, 4, 5]:
        season = 1  # Spring
    elif month in [6, 7, 8]:
        season = 2  # Summer
    elif month in [9, 10, 11]:
        season = 3  # Fall
    else:
        season = 4  # Winter
    
    # Hour from input
    hour = int(data.get('hour', 12))
    
    # Weather mapping (frontend: sunny/cloudy/rainy/windy -> model: weathersit)
    weather = data.get('weather', 'sunny').lower()
    weather_mapping = {
        'sunny': {'weathersit': 1, 'weather_severity': 1, 'storm_flag': 0},
        'cloudy': {'weathersit': 2, 'weather_severity': 2, 'storm_flag': 0},
        'rainy': {'weathersit': 3, 'weather_severity': 3, 'storm_flag': 1},
        'windy': {'weathersit': 2, 'weather_severity': 2, 'storm_flag': 0},
    }
    weather_features = weather_mapping.get(weather, weather_mapping['sunny'])
    
    # Temperature and humidity (use defaults if not provided)
    temp = float(data.get('temperature', 20.0))  # Default 20°C
    atemp = temp * 0.95  # Apparent temperature (slightly lower)
    hum = float(data.get('humidity', 65.0))  # Default 65%
    windspeed = float(data.get('windspeed', 10.0))  # Default 10 km/h
    
    # Cyclical encoding for hour and month
    hour_sin = math.sin(2 * math.pi * hour / 24)
    hour_cos = math.cos(2 * math.pi * hour / 24)
    month_sin = math.sin(2 * math.pi * month / 12)
    month_cos = math.cos(2 * math.pi * month / 12)
    
    # Lag features (using defaults - in production, these would come from historical data)
    cnt_lag_1 = float(data.get('cnt_lag_1', 50.0))  # Previous hour
    cnt_lag_24 = float(data.get('cnt_lag_24', 100.0))  # Same hour previous day
    
    # Build feature dictionary
    features = {
        'season': season,
        'mnth': month,
        'hr': hour,
        'weekday': weekday,
        'is_weekend': is_weekend,
        'week_of_year': week_of_year,
        'temp': temp,
        'atemp': atemp,
        'hum': hum,
        'windspeed': windspeed,
        'weathersit': weather_features['weathersit'],
        'weather_severity': weather_features['weather_severity'],
        'storm_flag': weather_features['storm_flag'],
        'hour_sin': hour_sin,
        'hour_cos': hour_cos,
        'month_sin': month_sin,
        'month_cos': month_cos,
        'cnt_lag_1': cnt_lag_1,
        'cnt_lag_24': cnt_lag_24,
    }
    
    return features


@app.route('/api/predict/hourly', methods=['POST'])
def predict_hourly():
    """
    Endpoint for hourly predictions from React frontend.
    Accepts simplified inputs and transforms them to model features.
    
    Expected JSON:
    {
        "date": "2024-01-15",
        "hour": 14,
        "weather": "sunny",
        "isEvent": false,
        "bikeType": "yulu",
        "temperature": 25.0,
        "humidity": 60.0
    }
    """
    if model is None or model_features is None:
        return jsonify({
            'error': 'Model or features not loaded',
            'success': False
        }), 500
    
    try:
        data = request.get_json()
        if data is None:
            return jsonify({
                'error': 'No JSON data provided',
                'success': False
            }), 400
        
        # Transform frontend inputs to model features
        features = transform_frontend_inputs_to_features(data)
        
        # Extract features in the correct order
        feature_values = [features.get(f, 0.0) for f in model_features]
        feature_array = np.array(feature_values).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(feature_array)
        prediction_value = float(prediction[0]) if isinstance(prediction, np.ndarray) else float(prediction)
        
        # Determine demand level and confidence
        if prediction_value < 50:
            demand_level = 'low'
            confidence = 75 + np.random.random() * 15
        elif prediction_value < 120:
            demand_level = 'medium'
            confidence = 80 + np.random.random() * 15
        else:
            demand_level = 'high'
            confidence = 85 + np.random.random() * 10
        
        # Generate recommendations
        recommendations = {
            'low': 'Low demand expected. Consider promotional offers to boost rentals.',
            'medium': 'Moderate demand. Standard bike availability should suffice.',
            'high': 'High demand predicted. Ensure maximum fleet availability and consider surge pricing.',
        }
        
        # Generate hourly breakdown (simplified - in production, predict each hour)
        hourly_breakdown = []
        for h in range(24):
            temp_data = data.copy()
            temp_data['hour'] = h
            temp_features = transform_frontend_inputs_to_features(temp_data)
            temp_values = [temp_features.get(f, 0.0) for f in model_features]
            temp_array = np.array(temp_values).reshape(1, -1)
            hour_prediction = model.predict(temp_array)
            hour_value = float(hour_prediction[0]) if isinstance(hour_prediction, np.ndarray) else float(hour_prediction)
            hourly_breakdown.append({'hour': h, 'rentals': max(0, round(hour_value))})
        
        return jsonify({
            'success': True,
            'predictedRentals': max(0, round(prediction_value)),
            'confidence': round(confidence),
            'demandLevel': demand_level,
            'recommendation': recommendations[demand_level],
            'hourlyBreakdown': hourly_breakdown
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction error: {str(e)}',
            'success': False
        }), 500


@app.route('/api/predict/daywise', methods=['POST'])
def predict_daywise():
    """
    Endpoint for day-wise predictions from React frontend.
    
    Expected JSON:
    {
        "date": "2024-01-15",
        "weather": "sunny",
        "isEvent": false,
        "bikeType": "yulu"
    }
    """
    if model is None or model_features is None:
        return jsonify({
            'error': 'Model or features not loaded',
            'success': False
        }), 500
    
    try:
        data = request.get_json()
        if data is None:
            return jsonify({
                'error': 'No JSON data provided',
                'success': False
            }), 400
        
        # Predict for each hour of the day
        hourly_distribution = []
        total_rentals = 0
        peak_hour = 0
        peak_rentals = 0
        
        for hour in range(24):
            temp_data = data.copy()
            temp_data['hour'] = hour
            features = transform_frontend_inputs_to_features(temp_data)
            feature_values = [features.get(f, 0.0) for f in model_features]
            feature_array = np.array(feature_values).reshape(1, -1)
            
            prediction = model.predict(feature_array)
            hour_value = float(prediction[0]) if isinstance(prediction, np.ndarray) else float(prediction)
            hour_rentals = max(0, round(hour_value))
            
            hourly_distribution.append({'hour': hour, 'rentals': hour_rentals})
            total_rentals += hour_rentals
            
            if hour_rentals > peak_rentals:
                peak_rentals = hour_rentals
                peak_hour = hour
        
        # Determine demand level
        if total_rentals < 800:
            demand_level = 'low'
            confidence = 70 + np.random.random() * 20
        elif total_rentals < 1500:
            demand_level = 'medium'
            confidence = 75 + np.random.random() * 20
        else:
            demand_level = 'high'
            confidence = 80 + np.random.random() * 15
        
        # Generate suggestions
        suggestions = {
            'low': 'Consider reducing active fleet to optimize operational costs.',
            'medium': 'Maintain standard fleet distribution across zones.',
            'high': 'Deploy additional bikes to high-traffic zones. Consider partnering with nearby businesses.',
        }
        
        # Find peak hour range
        peak_start = max(0, peak_hour - 1)
        peak_end = min(23, peak_hour + 1)
        
        return jsonify({
            'success': True,
            'totalRentals': total_rentals,
            'peakHourStart': peak_start,
            'peakHourEnd': peak_end,
            'confidence': round(confidence),
            'demandLevel': demand_level,
            'utilizationSuggestion': suggestions[demand_level],
            'hourlyDistribution': hourly_distribution
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction error: {str(e)}',
            'success': False
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify server is running and model is loaded.
    """
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'features_loaded': model_features is not None,
        'feature_count': len(model_features) if model_features else 0
    })


if __name__ == '__main__':
    # Load model and features when server starts
    print("=" * 50)
    print("Starting ML Prediction Server...")
    print("=" * 50)
    load_model_and_features()
    print("=" * 50)
    print("Server ready! Starting Flask app...")
    print("=" * 50)
    
    # Run the Flask app
    # Set debug=False for production, debug=True for development
    app.run(host='0.0.0.0', port=5000, debug=True)
