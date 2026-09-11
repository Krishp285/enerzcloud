import os
import pandas as pd
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Base directory for relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "loan_approval_dataset.csv")
if not os.path.exists(dataset_path):
    dataset_path = os.path.join(BASE_DIR, "loan-data.csv")

# Load Dataset
df = pd.read_csv(dataset_path)

# Handle dataset columns depending on file loaded
if 'loan_status' in df.columns or ' loan_status' in df.columns:
    col_target = ' loan_status' if ' loan_status' in df.columns else 'loan_status'
    df['total_assets_value'] = (
        df[' residential_assets_value'] + df[' commercial_assets_value'] +
        df[' luxury_assets_value'] + df[' bank_asset_value']
    )
    feature_cols = [' no_of_dependents', ' income_annum', ' loan_amount', ' loan_term', ' cibil_score', 'total_assets_value']
    df[col_target] = df[col_target].astype(str).str.lower().str.strip().map({'approved': 1, 'rejected': 0}).astype(int)
    X = df[feature_cols]
    y = df[col_target]
else:
    clean_data = df.dropna().copy()
    clean_data["Dependents"] = clean_data["Dependents"].replace("3+", "3").astype(int)
    clean_data["Loan_Status"] = (
        clean_data["Loan_Status"].astype(str).str.strip().str.lower().map({"y": 1, "n": 0})
    )
    feature_cols = ["Dependents", "ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term", "Credit_History"]
    X = clean_data[feature_cols]
    y = clean_data["Loan_Status"]

# Split Data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model Training & Evaluation (Logistic Regression, Decision Trees, Random Forest)
models = {
    "Logistic Regression": LogisticRegression(random_state=42),
    "Decision Tree": DecisionTreeClassifier(max_depth=10, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
}

best_model = None
best_accuracy = 0.0
best_model_name = ""

for name, model_instance in models.items():
    model_instance.fit(X_train_scaled, y_train)
    y_pred = model_instance.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy of {name}: {acc:.4f}")
    if name == "Random Forest" or acc > best_accuracy:
        if best_model_name != "Random Forest" or acc >= best_accuracy:
            best_accuracy = acc
            best_model = model_instance
            best_model_name = name

print(f"\nBest Model Selected: {best_model_name} with Accuracy: {best_accuracy:.4f}")


# Save Model and Scaler to backend directory
backend_dir = os.path.join(BASE_DIR, "backend")
os.makedirs(backend_dir, exist_ok=True)

joblib.dump(best_model, os.path.join(backend_dir, "model.pkl"))
joblib.dump(scaler, os.path.join(backend_dir, "scaler.pkl"))

print("Model and Scaler Saved Successfully to backend/")

