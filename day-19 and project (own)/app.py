"""
Streamlit UI — Loan Default Prediction System (Project 2)
Run: streamlit run app.py
"""

import os
import pickle
import numpy as np
import streamlit as st

# ── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Loan Default Prediction",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background: #0f1117; }

    /* Hero banner */
    .hero {
        background: linear-gradient(135deg, #9B2423 0%, #D44B1E 60%, #E67E22 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero h1 { color: #fff; font-size: 2rem; font-weight: 700; margin: 0; }
    .hero p  { color: rgba(255,255,255,0.85); margin: 0.5rem 0 0; font-size: 1rem; }

    /* Section card */
    .section-card {
        background: #1a1d26;
        border: 1px solid #2c2f3e;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .section-title {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #E67E22;
        margin-bottom: 1rem;
    }

    /* Result box */
    .result-approved {
        background: linear-gradient(135deg, #0D6A2E, #1a9a45);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        color: #fff;
    }
    .result-rejected {
        background: linear-gradient(135deg, #9B2423, #D44B1E);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        color: #fff;
    }
    .result-label { font-size: 2.2rem; font-weight: 700; margin: 0; }
    .result-sub   { font-size: 1rem; opacity: 0.85; margin-top: 0.4rem; }

    /* Metric badges */
    .metric-row { display: flex; gap: 1rem; margin-top: 1rem; }
    .metric-box {
        flex: 1;
        background: #22253a;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .metric-value { font-size: 1.6rem; font-weight: 700; color: #E67E22; }
    .metric-label { font-size: 0.75rem; color: #8b8fa8; margin-top: 0.2rem; }

    /* Divider */
    hr { border-color: #2c2f3e; }

    /* Streamlit button override */
    div.stButton > button {
        background: linear-gradient(135deg, #9B2423, #E67E22);
        color: white;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        width: 100%;
        transition: opacity 0.2s;
    }
    div.stButton > button:hover { opacity: 0.85; }
</style>
""", unsafe_allow_html=True)

# ── Load Model & Scaler ────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH  = os.path.join(BASE_DIR, "model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

@st.cache_resource
def load_artifacts():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        return None, None
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)
    return model, scaler

model, scaler = load_artifacts()

# ── Hero ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🏦 Loan Default Prediction</h1>
    <p>Enter applicant details below to predict default risk and loan eligibility</p>
</div>
""", unsafe_allow_html=True)

if model is None:
    st.error("Model artifacts not found. Please run `python task.py` first to train and save the model.")
    st.stop()

# ── Input Form ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Applicant Personal Information</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    gender = st.selectbox("Gender", ["Male", "Female"], key="gender")
with col2:
    married = st.selectbox("Married", ["Yes", "No"], key="married")
with col3:
    dependents = st.selectbox("Dependents", [0, 1, 2, 3], key="dependents",
                               help="Choose 3 for 3 or more dependents")

col4, col5 = st.columns(2)
with col4:
    education = st.selectbox("Education", ["Graduate", "Not Graduate"], key="education")
with col5:
    self_employed = st.selectbox("Self Employed", ["No", "Yes"], key="self_employed")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Financial Details</div>', unsafe_allow_html=True)

col6, col7 = st.columns(2)
with col6:
    applicant_income = st.number_input(
        "Applicant Monthly Income (₹)", min_value=0, max_value=100000,
        value=5000, step=500, key="applicant_income"
    )
with col7:
    coapplicant_income = st.number_input(
        "Co-applicant Monthly Income (₹)", min_value=0, max_value=50000,
        value=0, step=500, key="coapplicant_income"
    )

col8, col9 = st.columns(2)
with col8:
    loan_amount = st.number_input(
        "Loan Amount (₹ thousands)", min_value=1, max_value=700,
        value=128, step=10, key="loan_amount"
    )
with col9:
    loan_amount_term = st.selectbox(
        "Loan Term (months)", [12, 36, 60, 84, 120, 180, 240, 300, 360, 480],
        index=9, key="loan_term"
    )

col10, col11 = st.columns(2)
with col10:
    credit_history = st.selectbox(
        "Credit History", [1, 0],
        format_func=lambda x: "Good (1)" if x == 1 else "Bad (0)",
        key="credit_history"
    )
with col11:
    property_area = st.selectbox(
        "Property Area", ["Rural", "Semiurban", "Urban"],
        key="property_area"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ── Predict ─────────────────────────────────────────────────────────────────
if st.button("Predict Loan Default Risk"):

    # Encode inputs exactly as task.py does
    gender_enc       = 1 if gender == "Male" else 0
    married_enc      = 1 if married == "Yes" else 0
    education_enc    = 1 if education == "Graduate" else 0
    self_emp_enc     = 1 if self_employed == "Yes" else 0
    property_enc     = {"Rural": 0, "Semiurban": 1, "Urban": 2}[property_area]

    features = np.array([[
        gender_enc, married_enc, dependents, education_enc,
        self_emp_enc, applicant_income, coapplicant_income,
        loan_amount, loan_amount_term, credit_history, property_enc
    ]])

    features_scaled = scaler.transform(features)

    prediction   = model.predict(features_scaled)[0]
    probabilities = model.predict_proba(features_scaled)[0]

    approved_prob = probabilities[1]   # class 1 = Approved
    rejected_prob = probabilities[0]   # class 0 = Default / Rejected

    st.markdown("---")

    # Result card
    if prediction == 1:
        st.markdown(f"""
        <div class="result-approved">
            <div class="result-label">Loan Likely to be Repaid</div>
            <div class="result-sub">Low Default Risk — Application can proceed to approval stage</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-rejected">
            <div class="result-label">Loan at High Default Risk</div>
            <div class="result-sub">High Default Probability — Recommend rejection or enhanced due diligence</div>
        </div>
        """, unsafe_allow_html=True)

    # Probability meters
    st.markdown("### Probability Breakdown")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Repayment Probability", f"{approved_prob * 100:.2f}%")
        st.progress(float(approved_prob))
    with col_b:
        st.metric("Default Probability", f"{rejected_prob * 100:.2f}%")
        st.progress(float(rejected_prob))

    # Risk tier badge
    st.markdown("### Risk Classification")
    if approved_prob >= 0.75:
        st.success("**Tier 1 — Low Risk**: High confidence repayment. Auto-approve eligible.")
    elif approved_prob >= 0.45:
        st.warning("**Tier 2 — Moderate Risk**: Route to manual underwriter for review.")
    else:
        st.error("**Tier 3 — High Risk**: High default probability. Recommend auto-rejection.")

    # Raw values expander
    with st.expander("View raw probability values"):
        st.write({
            "Repayment Probability": round(float(approved_prob), 6),
            "Default Probability"  : round(float(rejected_prob), 6),
            "Prediction (0=Default, 1=Approved)": int(prediction)
        })

# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Loan Default Prediction System | Day-19 Project | Logistic Regression | loan-data.csv (614 records)")
