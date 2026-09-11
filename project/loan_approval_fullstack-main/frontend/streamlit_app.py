import streamlit as st
import requests
import os


BACKEND_URL = st.secrets.get("BACKEND_URL", os.getenv("BACKEND_URL", "http://127.0.0.1:8000")).rstrip("/")
if not BACKEND_URL.startswith(("http://", "https://")):
    BACKEND_URL = f"https://{BACKEND_URL}"

st.title("Loan Approval Prediction System")


# User Inputs
no_of_dependents = st.number_input("no of dependents", min_value=0)

income_annum = st.number_input("income annum", min_value=0)

loan_amount = st.number_input("loan amount", min_value=0)

loan_term = st.number_input("loan term", min_value=0)

cibil_score = st.number_input("cibil score", min_value=0)

total_assets_value = st.number_input("Total Assets Value", min_value=0)


# Predict Button
if st.button("Predict Loan Status"):

    payload = {
        "no_of_dependents": no_of_dependents,
        "income_annum": income_annum,
        "loan_amount": loan_amount,
        "loan_term": loan_term,
        "cibil_score": cibil_score,
        "total_assets_value": total_assets_value,
    }

    # API Call
    try:
        response = requests.post(f"{BACKEND_URL}/predict", json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as error:
        st.error(f"Prediction service is unavailable: {error}")
        st.stop()

    st.subheader(f"Prediction: {result['prediction']}")

    prob_val = float(result['approval_probability'])
    percent_str = result.get('approval_percentage', f"{round(prob_val * 100, 2)}%")

    st.write(f"**Approval Probability (Decimal)**: `{prob_val:.4f}`")
    st.write(f"**Approval Probability (Percentage)**: `{percent_str}`")
    st.progress(prob_val)

