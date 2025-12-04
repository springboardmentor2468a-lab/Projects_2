🚴‍♂️ RideWise – Bike Sharing Demand Prediction

📘 Overview
RideWise is a machine learning regression project that predicts bike-sharing demand using historical rental data, weather conditions, and event-related features. The goal is to forecast rental counts (cnt) to support better decision-making in urban bike-sharing systems.



📂 Dataset

Dataset from Kaggle containing:

Weather information

Date & time features

Holiday/working day indicators

Bike rental counts

🔗 Source: https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset





🧼 Data Preprocessing

Handling missing or inconsistent data

Encoding categorical variables

Feature engineering

Outlier detection & removal using IQR (Boxplot method)





📊 Exploratory Data Analysis (EDA)

Performed visual analysis including:

Histograms

Boxplots

Correlation insights

Distribution and trend analysis





🤖 Modeling
Regression techniques used to predict rental demand:

Linear Regression

Random Forest

Gradient Boosting

KNN

SVM

Target Variable: cnt

Input Features: Weather metrics, time/date attributes, event information.






📈 Evaluation

Models evaluated using:

MAE

RMSE

R² Score

Gradient Boosting achieved the best performance.






🛠 Tech Stack

Python

Pandas, NumPy

Matplotlib, Seaborn

Scikit-Learn
Jupyter Notebook
