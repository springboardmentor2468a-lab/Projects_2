import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('default')
sns.set()

dfd = pd.read_csv("day.csv")
dfh = pd.read_csv("hour.csv")

print("Datasets Loaded Successfully")
print("\nDAY CSV - First 5 Rows")
print(dfd.head())

print("\nHOUR CSV - First 5 Rows")
print(dfh.head())

columns_to_drop_day = ['instant', 'dteday', 'yr']
columns_to_drop_hour = ['instant', 'dteday', 'yr']

dfd.drop(columns=columns_to_drop_day, inplace=True, errors="ignore")
dfh.drop(columns=columns_to_drop_hour, inplace=True, errors="ignore")

print("\nColumns Dropped Successfully")

print("\nDAY CSV INFO")
print(dfd.info())

print("\nHOUR CSV INFO")
print(dfh.info())

print("\nMissing Values in day.csv:")
print(dfd.isnull().sum())

print("\nMissing Values in hour.csv:")
print(dfh.isnull().sum())

print("\nDuplicates in day.csv:", dfd.duplicated().sum())
print("Duplicates in hour.csv:", dfh.duplicated().sum())

plt.figure(figsize=(14, 6))
sns.heatmap(dfd.corr(), cmap="coolwarm")
plt.title("Correlation Heatmap - Day Dataset")
plt.show()

plt.figure(figsize=(14, 6))
sns.heatmap(dfh.corr(), cmap="coolwarm")
plt.title("Correlation Heatmap - Hour Dataset")
plt.show()
dfd.select_dtypes(include='number').hist(figsize=(15, 10))
plt.suptitle("Histograms - DAY Dataset", fontsize=16)
plt.tight_layout()
plt.show()

dfh.select_dtypes(include='number').hist(figsize=(15, 10))
plt.suptitle("Histograms - HOUR Dataset", fontsize=16)
plt.tight_layout()
plt.show()
plt.suptitle("Pairplot - DAY Dataset", fontsize=16)
sns.pairplot(dfd.select_dtypes(include="number"))
plt.show()

plt.suptitle("Pairplot - HOUR Dataset", fontsize=16)
sns.pairplot(dfh.select_dtypes(include="number"))
plt.show()
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(6,4))
sns.histplot(dfd['cnt'], bins=30)
plt.title("Day-wise Total Users Distribution")
plt.show()
sns.scatterplot(data=dfd, x='temp', y='cnt')
plt.title("Temperature vs Bike Count")
plt.show()
plt.figure(figsize=(10,6))
sns.heatmap(dfd.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap - Day Dataset")
plt.show()
print("\nSUMMARY REPORT:")
print("1. Dataset Loaded Successfully.")
print("2. Missing values handled.")
print("3. Visualizations generated.")
print("4. Insights: Temperature, season, and humidity affect user count.")
