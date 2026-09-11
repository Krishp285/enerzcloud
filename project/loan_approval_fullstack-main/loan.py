# %%
import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# Base directory for resolving relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, 'loan_approval_dataset.csv')

# %%
df = pd.read_csv(dataset_path)
df.head()
df.info()

# %%
df.columns
df = df[[' no_of_dependents',' income_annum',' loan_amount',' loan_term',' cibil_score', ' residential_assets_value', ' commercial_assets_value',
       ' luxury_assets_value', ' bank_asset_value',' loan_status']]

df.info()
df['total_assets_value'] = df[' residential_assets_value'] + df[' commercial_assets_value'] + df[' luxury_assets_value'] + df[' bank_asset_value']
df.info()
df.head()


# %%

df = df[[' no_of_dependents',' income_annum',' loan_amount',' loan_term',' cibil_score','total_assets_value',' loan_status']]
df.info()
df.head()
df[' loan_status'].value_counts()

# %%
df[' loan_status'] = df[' loan_status'].str.lower().str.strip().map({'approved': 1, 'rejected': 0}).astype(int)
df.info()
df

# %%
X=df[[' no_of_dependents',' income_annum',' loan_amount',' loan_term',' cibil_score', 'total_assets_value']]
Y=df[' loan_status']
X_train , X_test , Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
X_train.info()

# %%
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# %%
# Model Selection and Evaluation (Logistic Regression, Decision Trees, Random Forest)
models = {
    "Logistic Regression": LogisticRegression(random_state=42),
    "Decision Tree": DecisionTreeClassifier(max_depth=10, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
}

comparison_results = {}
best_model = None
best_accuracy = 0.0
best_model_name = ""

print("\n" + "="*65)
print(f"{'MODEL COMPARISON SUMMARY':^65}")
print("="*65)
print(f"{'Model Name':<22} | {'Accuracy':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10}")
print("-" * 65)

for name, model_instance in models.items():
    model_instance.fit(X_train_scaled, Y_train)
    Y_pred = model_instance.predict(X_test_scaled)
    
    acc = accuracy_score(Y_test, Y_pred)
    prec = precision_score(Y_test, Y_pred)
    rec = recall_score(Y_test, Y_pred)
    f1 = f1_score(Y_test, Y_pred)
    
    comparison_results[name] = {
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4)
    }
    
    print(f"{name:<22} | {acc:<10.4f} | {prec:<10.4f} | {rec:<10.4f} | {f1:<10.4f}")
    
    # Prefer Random Forest for smooth probability estimation if accuracies are comparable
    if name == "Random Forest" or acc > best_accuracy:
        if best_model_name != "Random Forest" or acc >= best_accuracy:
            best_accuracy = acc
            best_model = model_instance
            best_model_name = name

print("="*65)
print(f"\n>>> Best Model Selected for Production: {best_model_name} with Accuracy: {best_accuracy:.4f} <<<\n")


# %%
new_application = pd.DataFrame([
    {
        ' no_of_dependents': 2,
        ' income_annum': 50000,
        ' loan_amount': 200000,
        ' loan_term': 36,
        ' cibil_score': 750,
        'total_assets_value': 100000
    }])
new_application_scaled = scaler.transform(new_application)
prediction = best_model.predict(new_application_scaled)
probability = best_model.predict_proba(new_application_scaled)
print(prediction , probability)
print(f"Prediction for the new loan application: {'Approved' if prediction[0] == 1 else 'Rejected'}")
print(f"Probability of approval: {probability[0][1]:.2f} , Probability of rejection: {probability[0][0]:.2f}")


# Save Model & Scaler
backend_dir = os.path.join(BASE_DIR, "backend")
os.makedirs(backend_dir, exist_ok=True)
joblib.dump(best_model, os.path.join(backend_dir, "model.pkl"))
joblib.dump(scaler, os.path.join(backend_dir, "scaler.pkl"))

# Save Metrics Comparison JSON
metrics_data = {
    "dataset_rows": len(df),
    "best_model": best_model_name,
    "best_accuracy": round(float(best_accuracy), 4),
    "model_comparison": comparison_results,
    "features": list(X.columns)
}
with open(os.path.join(backend_dir, "metrics.json"), "w") as f:
    json.dump(metrics_data, f, indent=2)

print("Model, Scaler, and Metrics JSON saved successfully to backend/")