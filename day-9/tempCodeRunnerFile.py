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
