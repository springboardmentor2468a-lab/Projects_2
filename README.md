#  Bike Sharing Demand Forecasting

An end-to-end Machine Learning project to predict bike rental demand using time-series feature engineering and regression models.  
The project compares hour-level and day-level forecasting performance.

---

##  Project Objective

The goal of this project is to:

- Forecast bike rental demand accurately
- Capture seasonal and temporal patterns
- Reduce overfitting
- Compare hourly vs daily prediction performance

---

##  Dataset

The Bike Sharing Dataset includes:

- Date and time features  
- Weather conditions  
- Season and holiday indicators  
- Target variable: `cnt` (bike rental count)

Two modeling approaches were implemented:

-  **Hour-Level Dataset**
-  **Day-Level Dataset**

---

##  Feature Engineering

The following time-series features were created:

- Lag features (`cnt_lag1`, `cnt_lag2`, `cnt_lag7`)
- Rolling averages (3-day and 7-day)
- Cyclical encoding using sine and cosine transformation:
  - Month → `sin` / `cos`
  - Weekday → `sin` / `cos`
- Time-aware train-test split (`shuffle=False`) to prevent data leakage

---

##  Models Used

- Linear Regression  
- Random Forest Regressor  
- XGBoost Regressor (Best Performing Model)

---

##  Model Performance

### Hour-Level Model

- **R² (Train):** 0.91  
- **R² (Test):** 0.82  
- **Overfit Gap:** 0.09  

✔ Strong generalization  
✔ Low overfitting  

---

###  Day-Level Model

- **R² (Train):** 0.92  
- **R² (Test):** 0.70  
- **Overfit Gap:** 0.22  

⚠ Moderate overfitting due to smaller dataset size  

---

##  Tech Stack

- Python  
- Pandas  
- NumPy  
- Scikit-learn  
- XGBoost  
- Matplotlib  

---

Screenshot of Ridewise

<img width="1656" height="3584" alt="localhost_8501_(iPhone XR) (2)" src="https://github.com/user-attachments/assets/960b247d-a4ad-442d-b70a-09a20d227a72" />
<img width="2860" height="2376" alt="localhost_8501_(iPhone XR) (1)" src="https://github.com/user-attachments/assets/f4179ff1-5ca6-4a7e-a124-4d42df61ce0a" />

##  How to Run

```bash
git clone <your-repository-link>
cd RiseWise
pip install -r requirements.txt




