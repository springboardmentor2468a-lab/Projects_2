RideWise:Predicting Bike-Sharing Demand Based on Weather and Urban Events

Project Statement:
The goal of this project is to build machine learning regression models to predict city bike-sharing demand. The
primary objectives are to forecast daily or hourly rental counts for a city’s bike-sharing system based on a
combination of historical bike usage data, weather information, and details of city events or activities. This project
aims to help urban planners and transit operators make better decisions regarding fleet management and distribution
in response to demand patterns.
Use Cases: The project addresses two primary use cases:
Predicting Bike-Sharing Demand:
• Description: Using historical usage records, weather conditions, and scheduled city events, predict
the number of bike rentals for a given day or hour. This supports operational decisions in fleet
rebalancing, station stocking, and anticipating surges during special events or adverse weather.
Assessing Impact of Features:
• Description: Use the trained model to understand how factors such as weather variations, city events,
or neighbourhood characteristics affect demand. This helps in understanding and optimizing
ridership patterns and planning for infrastructure improvements.
Outcomes:
By the end of this project, students will:
• Understand the principles of data preprocessing, model building, and evaluation for regression
problems with real-world, messy data.
• Develop a regression model to predict bike-sharing demand using multi-source features. •
Implement and compare multiple regression methods and assess their accuracy.
• Prepare detailed documentation and a presentation of their findings and results.
Dataset: https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset?select=hour.csv
Model Architecture:
Modules to be implemented
1. Data preprocessing and feature selection.
• The data available in the dataset may have missing values, inconsistent entries, or categorical
variables with high cardinality.
• The first step is to clean and prepare the data, including handling missing values and encoding
categorical features such as event type or location.
• New columns/features, such as ‘is_holiday’ or ‘event_present,’ may be engineered based on the raw
data to improve model performance.
2. Building a Regression model
• Regression analysis will be used to predict the quantitative outcome, which is the number of bike
rentals for a specific date and time.
• The features (X) will include information such as date, time, weather data, event information, and
location. The target variable (y) will be daily or hourly bike rental counts.
3. Evaluation and Fine-tuning
• The regression model’s performance will be evaluated using metrics such as Mean Absolute Error
(MAE), Root Mean Squared Error (RMSE), and R-squared.
• Hyperparameters and feature engineering techniques will be adjusted to improve prediction
accuracy. Feature importance can also be assessed to understand which variables most affect
demand.
4. Documentation and Presentation Preparation
• Prepare thorough documentation and visualizations summarizing the project, methodology, results,
and interpretations. Present insights on how various external factors impact bike-sharing demand.
Week-wise module implementation and high-level requirements with output screenshots
Milestone 1:
Week 1: Project Initialization and Dataset Acquisition.
• Understand project objectives and outcomes.
• Source and collect public datasets on bike-sharing usage, city weather, and event schedules. •
Explore the structure and quality of each dataset; examine available columns and data samples.
Week 2: Data Preprocessing and Feature Selection.
• Clean and merge datasets; address missing values, data inconsistencies, and formatting issues. •
Select and engineer relevant features required for modelling, such as time variables, weather
metrics, and event presence.
Milestone 2:
Week 3: Preliminary Model Training.
• Implement early regression models and train on processed data.
• Analyse initial model performance and identify areas for data or model improvement.
Week 4: Predictions and Fine-tuning the Model.
• Generate preliminary predictions and evaluate results.
• Tweak preprocessing or modelling pipeline (e.g., encode features differently, adjust model
parameters) to enhance performance.
Milestone 3:
Week 5: Refine Data and Experiment with Model Architectures.
• Investigate further data improvements and explore additional model types or feature sets. •
Retrain and compare results, documenting gains and differences between models.
Week 6: Inference with Test Data.
• Apply the final model to a hold-out or new portion of data to simulate real-world predictions. •
Assess performance and, if necessary, revisit earlier steps for additional tuning.
Milestone 4:
Week 7: Build a Full Stack Application for Model Use
• To facilitate practical use, develop a simple web interface allowing users to input date, location, event, and
weather details and receive demand predictions.
• Integrate pipeline for preprocessing and prediction in the backend and make the solution accessible.
Week 8: Documentation, Presentation, and Demo Preparation
• Compile complete documentation covering methodology, results, and conclusions.
• Prepare a summary presentation explaining the project’s workflow, findings, and operational
recommendations.
Evaluation Criteria:
1. Completion of Milestones: Assess each milestone's completion within its timeframe. Successful acquisition,
cleaning, integration, modelling, and presentation must be evident for project success.
2. Accuracy of the Predictions: Benchmark model predictions against actual recorded demand for selected
future periods or test data. The closer the predictions are to actuals, the better.
3. Clarity and Depth of Documentation and Presentation: Review documentation for completeness, clarity,
and technical soundness. Assess the final presentation for its ability to communicate the project’s process,
findings, and relevance, supported by professional visualizations and explanations.
Model Performance - Quantitative Metrics:
• Bike Demand Prediction
o Metric: Mean Absolute Error (MAE)
o Description: Measures the average absolute difference between the model’s predicted and actual
number of bike rentals for a given period. Lower MAE values indicate better model accuracy.
Additional Training Metrics:
• Metric: Loss Curves (Training and Validation Loss)
• Description: Track the loss during training and validation stages to ensure proper learning, detect overfitting,
and assess model improvements as refinements are made.
Example Quantitative Metrics for Evaluation
1. Bike-Sharing Demand Prediction
• Goal: Achieve as low as possible loss values on training and test data, demonstrating a reliable and
generalizable model.
