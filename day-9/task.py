# Assignment Title: House Price Prediction with Linear Regression

# Dataset: housing.csv or Kaggle housing data

# Train a multiple linear regression model

# Evaluate model using all metrics

# Save the model using joblib

# Plot at least:

# Regression Line (Simple)

# Actual vs Predicted

# Residual Plot


from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error , mean_absolute_error , root_mean_squared_error
import matplotlib.pyplot as plt

housing = fetch_california_housing()
model = LinearRegression()
model.fit(housing.data, housing.target)

# Make predictions
y_pred = model.predict(housing.data)

# Evaluate the model
mse = mean_squared_error(housing.target, y_pred)
mae = mean_absolute_error(housing.target, y_pred)
rmse = root_mean_squared_error(housing.target, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"Mean Absolute Error: {mae}")
print(f"Root Mean Squared Error: {rmse}")

plt.plot(housing.target, y_pred, 'o')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs Predicted Values')
plt.show()


# student_scores.csv project 
import pandas as pd

df = pd.read_csv('C:\\Users\\DELL\\OneDrive\\Desktop\\enerzcloud\\day-9\\student-scores.csv')
print(df.head())

for col in ['part_time_job', 'extracurricular_activities']:
    df[col] = df[col].astype(str).str.strip().str.lower().map({
        'yes': 1,
        'no': 0,
        'true': 1,
        'false': 0,
    }).fillna(0).astype(int)

X = df[[
    'part_time_job',
    'absence_days',
    'extracurricular_activities',
    'weekly_self_study_hours',
    'math_score',
    'history_score',
    'physics_score',
    'chemistry_score',
    'biology_score',
    'english_score',
    'geography_score'
]].copy()
X = X.fillna(0)
Y = df['final_score'].astype(float)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(x_train, y_train)

predictions = model.predict(x_test)
print(predictions)
print('R^2:', model.score(x_test, y_test))
