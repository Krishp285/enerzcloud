# %%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

print("=========================================================")
print("  PROJECT: LOAN DEFAULT PREDICTION SYSTEM                ")
print("=========================================================\n")

# %% =======================================================
# PHASE 1: DATA LOADING & PREPROCESSING
# ==========================================================
print("--- PHASE 1: DATA PREPROCESSING ---")

# Dynamic path resolution to loan-data.csv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, '..', 'project', 'loan_approval_fullstack-main', 'loan-data.csv')
if not os.path.exists(data_path):
    data_path = r'C:\Users\DELL\OneDrive\Desktop\enerzcloud\project\loan_approval_fullstack-main\loan-data.csv'

df = pd.read_csv(data_path)
print(f"Dataset Loaded Successfully! Rows: {df.shape[0]}, Columns: {df.shape[1]}")

# 1. Remove unnecessary columns like Loan_ID
if 'Loan_ID' in df.columns:
    df = df.drop('Loan_ID', axis=1)
    print("[OK] Removed Loan_ID column.")


# 2. Handle Missing Values
print("\nMissing values before imputation:")
print(df.isnull().sum()[df.isnull().sum() > 0])

# Impute Categorical variables with Mode
df['Gender'] = df['Gender'].fillna(df['Gender'].mode()[0])
df['Married'] = df['Married'].fillna(df['Married'].mode()[0])
df['Dependents'] = df['Dependents'].fillna(df['Dependents'].mode()[0])
df['Self_Employed'] = df['Self_Employed'].fillna(df['Self_Employed'].mode()[0])
df['Credit_History'] = df['Credit_History'].fillna(df['Credit_History'].mode()[0])

# Impute Numerical variables with Median
df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].median())
df['Loan_Amount_Term'] = df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].median())

print("[OK] Missing values successfully imputed.")

# 3. Categorical Data Encoding
df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})
df['Married'] = df['Married'].map({'Yes': 1, 'No': 0})
df['Education'] = df['Education'].map({'Graduate': 1, 'Not Graduate': 0})
df['Self_Employed'] = df['Self_Employed'].map({'Yes': 1, 'No': 0})

# Dependents encoding (convert '3+' to 3)
df['Dependents'] = df['Dependents'].replace('3+', 3).astype(int)

# Property_Area ordinal/label encoding
df['Property_Area'] = df['Property_Area'].map({'Rural': 0, 'Semiurban': 1, 'Urban': 2})

# Target Column Encoding: Loan_Status (Y -> 1, N -> 0)
df['Loan_Status'] = df['Loan_Status'].astype(str).str.strip().str.upper().map({'Y': 1, 'N': 0})

print("[OK] Categorical features and Target column successfully encoded.")


# %% =======================================================
# PHASE 2: EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================================
print("\n--- PHASE 2: EXPLORATORY DATA ANALYSIS (EDA) ---")
print("\nSummary Statistics of Processed Dataset:")
print(df.describe())

# EDA Visualization Plots
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
fig.suptitle('Loan Default Prediction - Exploratory Data Analysis', fontsize=14, fontweight='bold')

# Plot 1: Loan Amount Distribution
sns.histplot(df['LoanAmount'], kde=True, ax=axes[0, 0], color='skyblue')
axes[0, 0].set_title('Loan Amount Distribution')
axes[0, 0].set_xlabel('Loan Amount')

# Plot 2: Applicant Income Distribution
sns.histplot(df['ApplicantIncome'], kde=True, ax=axes[0, 1], color='salmon')
axes[0, 1].set_title('Applicant Income Distribution')
axes[0, 1].set_xlabel('Applicant Income')

# Plot 3: Credit History vs Loan Status
sns.countplot(x='Credit_History', hue='Loan_Status', data=df, ax=axes[1, 0], palette='Set2')
axes[1, 0].set_title('Credit History vs Loan Status')
axes[1, 0].set_xlabel('Credit History (0 = Bad, 1 = Good)')
axes[1, 0].set_ylabel('Count')

# Plot 4: Property Area vs Loan Status
sns.countplot(x='Property_Area', hue='Loan_Status', data=df, ax=axes[1, 1], palette='Set1')
axes[1, 1].set_title('Property Area vs Loan Status (0=Rural, 1=Semiurban, 2=Urban)')
axes[1, 1].set_xlabel('Property Area')
axes[1, 1].set_ylabel('Count')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
eda_fig_path = os.path.join(BASE_DIR, 'eda_plots.png')
plt.savefig(eda_fig_path)
print(f"[OK] EDA plots saved to {eda_fig_path}")
plt.close()

# Correlation Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, fmt='.2f', cmap='Blues')
plt.title('Feature Correlation Heatmap')
plt.tight_layout()
heatmap_path = os.path.join(BASE_DIR, 'correlation_heatmap.png')
plt.savefig(heatmap_path)
print(f"[OK] Correlation heatmap saved to {heatmap_path}")
plt.close()


# %% =======================================================
# PHASE 3: MODEL BUILDING & EVALUATION
# ==========================================================
print("\n--- PHASE 3: MODEL BUILDING & EVALUATION ---")

# Separate Features (X) and Target (y)
X = df.drop('Loan_Status', axis=1)
y = df['Loan_Status']

# Train-Test Split (80-20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature Scaling using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Models to Train
models = {
    'Logistic Regression': LogisticRegression(random_state=42),
    'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
}

results = {}

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    results[name] = {
        'Accuracy': acc,
        'Precision': prec,
        'Recall': rec,
        'F1 Score': f1,
        'Confusion Matrix': cm
    }
    
    print(f"\n[{name}] Results:")
    print(f"  - Accuracy : {acc:.4f}")
    print(f"  - Precision: {prec:.4f}")
    print(f"  - Recall   : {rec:.4f}")
    print(f"  - F1 Score : {f1:.4f}")
    print(f"  - Confusion Matrix:\n{cm}")


# %% =======================================================
# PHASE 4: MODEL COMPARISON
# ==========================================================
print("\n--- PHASE 4: MODEL COMPARISON ---")

comparison_df = pd.DataFrame({
    'Model': list(results.keys()),
    'Accuracy': [results[m]['Accuracy'] for m in results],
    'Precision': [results[m]['Precision'] for m in results],
    'Recall': [results[m]['Recall'] for m in results],
    'F1 Score': [results[m]['F1 Score'] for m in results]
})

print("\n" + "="*70)
print(f"{'MODEL COMPARISON TABLE':^70}")
print("="*70)
print(comparison_df.to_string(index=False))
print("="*70)

best_model_name = comparison_df.sort_values(by='Accuracy', ascending=False).iloc[0]['Model']
best_acc = comparison_df.sort_values(by='Accuracy', ascending=False).iloc[0]['Accuracy']
print(f"\n[BEST MODEL] BEST PERFORMING MODEL: {best_model_name} with Accuracy = {best_acc:.4f}\n")


# Model Comparison Bar Plot
plt.figure(figsize=(10, 6))
metrics_plot = comparison_df.set_index('Model')
metrics_plot.plot(kind='bar', figsize=(10, 6), colormap='viridis')
plt.title('Model Performance Metrics Comparison')
plt.xlabel('Algorithm')
plt.ylabel('Score (0.0 - 1.0)')
plt.ylim([0.5, 1.0])
plt.legend(loc='lower right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
comparison_fig_path = os.path.join(BASE_DIR, 'model_comparison.png')
plt.savefig(comparison_fig_path)
print(f"[OK] Model comparison plot saved to {comparison_fig_path}")
plt.close()

# %% =======================================================
# SAVE BEST MODEL & SCALER FOR STREAMLIT APP
# ==========================================================
import pickle

best_model_obj = models[best_model_name]
model_save_path  = os.path.join(BASE_DIR, 'model.pkl')
scaler_save_path = os.path.join(BASE_DIR, 'scaler.pkl')

with open(model_save_path, 'wb') as f:
    pickle.dump(best_model_obj, f)
with open(scaler_save_path, 'wb') as f:
    pickle.dump(scaler, f)

print(f"[OK] Best model ({best_model_name}) saved to {model_save_path}")
print(f"[OK] Scaler saved to {scaler_save_path}")
print("\nRun the Streamlit UI with: streamlit run app.py")