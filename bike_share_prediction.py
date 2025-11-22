import os
print("Current Working Directory:", os.getcwd())
print("Files in Directory:", os.listdir('.'))
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
day = pd.read_csv('day.csv')
hour = pd.read_csv('hour.csv')
print("Day File Sample:")
print(day.head())
print("Hour File Sample:")
print(hour.head())
plt.scatter(day['temp'], day['cnt'])
plt.xlabel('Temperature')
plt.ylabel('Rental Count')
plt.title('Daily Rentals vs Temperature')
plt.show()
plt.plot(hour.groupby('hr')['cnt'].mean())
plt.xlabel('Hour of Day')
plt.ylabel('Average Rentals')
plt.title('Hourly Rental Pattern')
plt.show()
features = ['temp', 'humidity', 'windspeed', 'season', 'holiday', 'workingday', 'hr']
X = hour[features]
y = hour['cnt']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print( "Test Mean Squared Error:", mse)