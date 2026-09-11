"""
PROJECT 2: Loan Default Prediction System
Generates:
  - Loan_Default_Report.docx
  - Loan_Default_Presentation.pptx
  (Updated to include Streamlit UI section)
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

from pptx import Presentation
from pptx.util import Inches as PI, Pt as PPt
from pptx.dml.color import RGBColor as PRC
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCX_OUT = os.path.join(BASE_DIR, "Loan_Default_Report.docx")
PPTX_OUT = os.path.join(BASE_DIR, "Loan_Default_Presentation.pptx")

# ── Helpers ─────────────────────────────────────────────────────────────────
def shade_cell(cell, hex_color):
    cell._tc.get_or_add_tcPr().append(
        parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))

def cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val)); node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)

def doc_h(doc, text, level, rgb=(155, 36, 35)):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = RGBColor(*rgb)
    return h

# ══════════════════════════════════════════════════════════════════════════════
#  WORD DOCUMENT
# ══════════════════════════════════════════════════════════════════════════════
def build_docx():
    print("Generating Loan_Default_Report.docx ...")
    doc = Document()
    for sec in doc.sections:
        sec.top_margin = sec.bottom_margin = Inches(1)
        sec.left_margin = sec.right_margin = Inches(1)

    # Cover
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("LOAN DEFAULT PREDICTION SYSTEM")
    r.font.name, r.font.size, r.font.bold = "Arial", Pt(24), True
    r.font.color.rgb = RGBColor(155, 36, 35)

    p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run("4-Phase ML Pipeline  +  Streamlit Web UI  |  loan-data.csv  (614 records)\n")
    r2.font.name, r2.font.size, r2.font.italic = "Arial", Pt(13), True
    r2.font.color.rgb = RGBColor(89, 89, 89)

    # 1. Executive Summary
    doc_h(doc, "1. Executive Summary", 1)
    doc.add_paragraph(
        "This report documents the complete Loan Default Prediction System: a 4-phase machine "
        "learning pipeline (day-19/task.py) combined with an interactive Streamlit web application "
        "(day-19/app.py). Operating on loan-data.csv (614 customer records, 13 features), the system "
        "trains three classification algorithms and deploys the best-performing model in a real-time "
        "browser-accessible UI with continuous probability scoring and tiered risk classification."
    )
    tbl = doc.add_table(1, 1); tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.cell(0, 0); shade_cell(c, "FDECEA"); cell_margins(c, 150, 150, 200, 200)
    bp = c.paragraphs[0]
    r_k = bp.add_run("KEY RESULT: "); r_k.font.bold, r_k.font.color.rgb = True, RGBColor(155, 36, 35)
    bp.add_run("Logistic Regression selected as production model — ")
    for bold_text in ["78.86% Accuracy", " · ", "85.87% F1-Score", " · ", "98.75% Recall"]:
        r_b = bp.add_run(bold_text); r_b.font.bold = (bold_text != " · ")

    # 2. Problem Definition
    doc_h(doc, "2. Problem Definition", 1)
    doc.add_paragraph(
        "Loan defaults create significant Non-Performing Assets (NPAs) for lending institutions. "
        "Identifying likely defaulters before disbursement enables proactive risk management."
    )
    for item in [
        "Business Goal: Minimize NPA losses by automatically flagging high-risk loan applications.",
        "Target Variable: Loan_Status — Y (Approved = 1) / N (Rejected / Default = 0).",
        "Dataset: loan-data.csv — 614 customer records, 13 columns including demographic & financial features.",
    ]:
        doc.add_paragraph(item, style="List Bullet")

    # 3. Dataset & Features
    doc_h(doc, "3. Dataset Overview & Raw Features", 1)
    feat_tbl = doc.add_table(14, 3); feat_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ci, h in enumerate(["Feature", "Type / Missing", "Description & Encoding"]):
        c = feat_tbl.rows[0].cells[ci]; c.text = h
        shade_cell(c, "9B2423")
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    features = [
        ("Loan_ID",          "String (Dropped)",       "Non-predictive unique ID — removed in Phase 1"),
        ("Gender",           "Categorical (13 miss.)", "Male=1, Female=0"),
        ("Married",          "Categorical (3 miss.)",  "Yes=1, No=0"),
        ("Dependents",       "Ordinal (15 miss.)",     "0/1/2/3+ — 3+ mapped to integer 3"),
        ("Education",        "Categorical",            "Graduate=1, Not Graduate=0"),
        ("Self_Employed",    "Categorical (32 miss.)", "Yes=1, No=0"),
        ("ApplicantIncome",  "Integer",                "Monthly income of the primary applicant (₹)"),
        ("CoapplicantIncome","Float",                  "Monthly income of co-applicant (₹)"),
        ("LoanAmount",       "Float (22 miss.)",       "Loan principal in ₹ thousands — median imputed"),
        ("Loan_Amount_Term", "Float (14 miss.)",       "Loan duration in months — median imputed"),
        ("Credit_History",   "Binary (50 miss.)",      "1=Good history, 0=Bad — mode imputed"),
        ("Property_Area",    "Ordinal",                "Rural=0, Semiurban=1, Urban=2"),
        ("Loan_Status",      "Target",                 "Y=1 (Approved) / N=0 (Default/Rejected)"),
    ]
    for ri, row in enumerate(features, 1):
        for ci, val in enumerate(row):
            feat_tbl.rows[ri].cells[ci].text = val
            cell_margins(feat_tbl.rows[ri].cells[ci], 80, 80, 100, 100)

    # 4. Phase 1 — Preprocessing
    doc_h(doc, "4. Phase 1 — Data Preprocessing", 1)
    doc_h(doc, "4.1 Column Removal", 2)
    doc.add_paragraph("Dropped Loan_ID (non-predictive unique identifier).")
    doc_h(doc, "4.2 Missing Value Imputation", 2)
    imp_tbl = doc.add_table(8, 4); imp_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ci, h in enumerate(["Column", "Missing Count", "Method", "Rationale"]):
        c = imp_tbl.rows[0].cells[ci]; c.text = h
        shade_cell(c, "9B2423")
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    imp_rows = [
        ("Gender", "13", "Mode", "Preserves dominant category"),
        ("Married / Dependents / Self_Employed", "3 / 15 / 32", "Mode", "Most frequent value is the safe default"),
        ("LoanAmount", "22", "Median", "Right-skewed — median is robust to outliers"),
        ("Loan_Amount_Term", "14", "Median", "360 months dominates the distribution"),
        ("Credit_History", "50", "Mode", "1.0 (Good) is the mode — safest assumption"),
    ]
    for ri, row in enumerate(imp_rows, 1):
        for ci, val in enumerate(row):
            imp_tbl.rows[ri].cells[ci].text = val
            cell_margins(imp_tbl.rows[ri].cells[ci], 80, 80, 100, 100)
    doc_h(doc, "4.3 Feature Scaling", 2)
    doc.add_paragraph("StandardScaler applied to all 11 predictor features before model training.")

    # 5. Phase 2 — EDA
    doc_h(doc, "5. Phase 2 — Exploratory Data Analysis", 1)
    doc.add_paragraph("Generated and saved to day-19 directory: eda_plots.png, correlation_heatmap.png, model_comparison.png")
    for finding in [
        "Credit_History: Single strongest binary predictor — applicants with history=1 have >80% approval rate.",
        "Property_Area: Semiurban owners have highest approval; Rural applicants have lowest.",
        "ApplicantIncome: Moderate positive correlation with approval.",
        "LoanAmount: Right-skewed distribution — confirms median imputation was the correct strategy.",
    ]:
        doc.add_paragraph(finding, style="List Bullet")

    # 6. Phase 3 & 4 — Models
    doc_h(doc, "6. Phase 3 & 4 — Model Training, Evaluation & Comparison", 1)
    doc.add_paragraph("Train/Test Split: 80% training (491 samples) / 20% testing (123 samples), random_state=42.")
    bench = doc.add_table(4, 6); bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ci, h in enumerate(["Model Algorithm", "Accuracy", "Precision", "Recall", "F1-Score", "Confusion Matrix"]):
        c = bench.rows[0].cells[ci]; c.text = h
        shade_cell(c, "9B2423")
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    model_rows = [
        ("Logistic Regression (Selected)", "78.86%", "75.96%", "98.75%", "85.87%", "[[18,25],[1,79]]"),
        ("Decision Tree Classifier",       "74.80%", "75.26%", "91.25%", "82.49%", "[[19,24],[7,73]]"),
        ("Random Forest Classifier",       "77.24%", "75.49%", "96.25%", "84.62%", "[[18,25],[3,77]]"),
    ]
    for ri, row in enumerate(model_rows, 1):
        for ci, val in enumerate(row):
            c = bench.rows[ri].cells[ci]; c.text = val
            cell_margins(c, 80, 80, 80, 80)
            if ri == 1:
                shade_cell(c, "FDECEA")
                c.paragraphs[0].runs[0].font.bold = True
    doc.add_paragraph(
        "\nModel Selection Rationale: Logistic Regression's 98.75% Recall minimizes missed defaulters "
        "(False Negatives = 1 only) — the most costly error in credit risk management."
    )

    # 7. Streamlit UI
    doc_h(doc, "7. Streamlit Interactive Web Application (app.py)", 1)
    doc.add_paragraph(
        "An interactive Streamlit web dashboard (day-19/app.py) provides a browser-accessible "
        "interface for real-time loan default risk prediction. The UI loads the pre-trained "
        "Logistic Regression model (model.pkl) and StandardScaler (scaler.pkl) saved by task.py."
    )
    doc_h(doc, "7.1 How to Run", 2)
    p_code = doc.add_paragraph()
    r_code = p_code.add_run("# Step 1: Train model and save artifacts\npython task.py\n\n# Step 2: Launch Streamlit UI\nstreamlit run app.py")
    r_code.font.name, r_code.font.size = "Courier New", Pt(10)
    r_code.font.color.rgb = RGBColor(31, 78, 120)

    doc_h(doc, "7.2 UI Features", 2)
    for feat in [
        "Personal Information inputs: Gender, Married, Dependents, Education, Self_Employed (dropdowns).",
        "Financial Detail inputs: ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area.",
        "Real-time Prediction: Approved/Rejected result card with color-coded visual feedback.",
        "Continuous Probability Bars: Separate progress bars showing exact Repayment % and Default % probabilities.",
        "Tiered Risk Classification: Tier 1 (Low Risk >= 75%), Tier 2 (Moderate 45–74%), Tier 3 (High Risk < 45%).",
        "Raw probability expander showing full floating-point probability values for audit purposes.",
    ]:
        doc.add_paragraph(feat, style="List Bullet")

    # 8. Business Recommendations
    doc_h(doc, "8. Business Recommendations", 1)
    for rec in [
        "Maximize Recall: Logistic Regression's 98.75% Recall ensures near-zero missed defaulters — prioritize this metric over pure accuracy.",
        "Credit History Enforcement: Mandate credit history documentation for all applicants — 50 missing records create scoring blind spots.",
        "Semiurban Incentives: Semiurban applicants show the highest repayment rates — offer preferential interest rate tiers for this segment.",
        "Streamlit Integration: Deploy app.py on an internal corporate server or Streamlit Cloud for branch-level officer access.",
        "Scale Model Upgrade: When dataset exceeds 5,000 records, evaluate XGBoost or LightGBM for improved performance on imbalanced data.",
    ]:
        doc.add_paragraph(rec, style="List Number")

    doc.save(DOCX_OUT)
    print(f"Saved: {DOCX_OUT}")


# ══════════════════════════════════════════════════════════════════════════════
#  POWERPOINT PRESENTATION
# ══════════════════════════════════════════════════════════════════════════════
def build_pptx():
    print("Generating Loan_Default_Presentation.pptx ...")
    prs = Presentation()
    prs.slide_width, prs.slide_height = PI(13.333), PI(7.5)
    blank = prs.slide_layouts[6]

    RED   = PRC(155, 36, 35)
    DARK  = PRC(60, 15, 15)
    WHITE = PRC(255, 255, 255)
    GRAY  = PRC(89, 89, 89)
    LGRAY = PRC(242, 244, 247)
    GOLD  = PRC(230, 150, 0)
    LRED  = PRC(253, 236, 234)

    def header(slide, title, subtitle="PROJECT 2: LOAN DEFAULT PREDICTION SYSTEM"):
        tb = slide.shapes.add_textbox(PI(0.8), PI(0.25), PI(11.7), PI(1.1))
        tf = tb.text_frame; tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = subtitle
        p1.font.name, p1.font.size, p1.font.bold, p1.font.color.rgb = "Arial", PPt(9), True, GOLD
        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name, p2.font.size, p2.font.bold, p2.font.color.rgb = "Arial", PPt(24), True, RED

    # SLIDE 1 — Title
    s = prs.slides.add_slide(blank)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, PI(13.333), PI(7.5))
    bg.fill.solid(); bg.fill.fore_color.rgb = DARK; bg.line.fill.background()
    tb = s.shapes.add_textbox(PI(1.0), PI(1.6), PI(11.3), PI(4.5))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "LOAN DEFAULT PREDICTION SYSTEM"
    p.font.name, p.font.size, p.font.bold, p.font.color.rgb = "Arial", PPt(34), True, WHITE
    p2 = tf.add_paragraph()
    p2.text = "4-Phase ML Pipeline  +  Streamlit Web UI  ·  614 Records  ·  loan-data.csv"
    p2.font.name, p2.font.size, p2.font.color.rgb = "Arial", PPt(15), GOLD; p2.space_before = PPt(12)
    p3 = tf.add_paragraph()
    p3.text = "Logistic Regression  ·  78.86% Accuracy  ·  98.75% Recall  ·  85.87% F1-Score"
    p3.font.name, p3.font.size, p3.font.color.rgb = "Arial", PPt(13), PRC(220, 180, 180); p3.space_before = PPt(24)

    # SLIDE 2 — Problem & Objective
    s2 = prs.slides.add_slide(blank)
    header(s2, "Problem Statement & Project Objective")
    cards = [
        ("BUSINESS PROBLEM", "Loan defaults create NPAs. Identifying likely defaulters before disbursement prevents financial losses and enables proactive risk management."),
        ("ML OBJECTIVE", "Binary classification: Predict Loan_Status (Y=Repay, N=Default) from 12 financial and demographic features using a 4-phase pipeline."),
        ("SYSTEM DESIGN", "Task.py pipeline trains and exports model.pkl + scaler.pkl. App.py loads these for real-time Streamlit UI prediction."),
    ]
    for i, (h, b) in enumerate(cards):
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PI(0.8 + i * 4.04), PI(1.55), PI(3.64), PI(5.2))
        card.fill.solid(); card.fill.fore_color.rgb = LRED; card.line.color.rgb = RED
        tf = card.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = h; p.font.bold, p.font.size, p.font.color.rgb = True, PPt(13), RED
        pb = tf.add_paragraph(); pb.text = b; pb.font.size, pb.font.color.rgb = PPt(12), GRAY; pb.space_before = PPt(14)

    # SLIDE 3 — Dataset Overview
    s3 = prs.slides.add_slide(blank)
    header(s3, "Dataset Overview — loan-data.csv")
    tb = s3.shapes.add_textbox(PI(0.8), PI(1.6), PI(5.8), PI(5.1))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "DATASET PROFILE"
    p.font.bold, p.font.color.rgb, p.font.size = True, RED, PPt(14)
    for item in ["Records: 614 customer loan applications", "Columns: 13 (12 features + Loan_Status target)",
                 "Class Split: 68.7% Approved / 31.3% Rejected", "Train / Test: 80% / 20% (random_state=42)",
                 "Missing Values: 7 columns with missing data"]:
        pb = tf.add_paragraph(); pb.text = "• " + item
        pb.font.size, pb.font.color.rgb = PPt(12), GRAY; pb.space_before = PPt(8)
    tb2 = s3.shapes.add_textbox(PI(6.8), PI(1.6), PI(5.7), PI(5.1))
    tf2 = tb2.text_frame; tf2.word_wrap = True
    p = tf2.paragraphs[0]; p.text = "MISSING VALUE IMPUTATION"
    p.font.bold, p.font.color.rgb, p.font.size = True, RED, PPt(14)
    for item in ["Credit_History: 50 (8.1%) → Mode imputed", "Self_Employed: 32 (5.2%) → Mode imputed",
                 "Dependents: 15 (2.4%) → Mode imputed", "LoanAmount: 22 (3.6%) → Median imputed",
                 "Loan_Amount_Term: 14 → Median imputed", "Gender: 13 → Mode imputed", "Married: 3 → Mode imputed"]:
        pb = tf2.add_paragraph(); pb.text = "• " + item
        pb.font.size, pb.font.color.rgb = PPt(11), GRAY; pb.space_before = PPt(6)

    # SLIDE 4 — Phase 1: Preprocessing
    s4 = prs.slides.add_slide(blank)
    header(s4, "Phase 1 — Data Preprocessing Pipeline")
    steps = [
        ("STEP 1: REMOVE Loan_ID", "Dropped non-predictive unique identifier to prevent data leakage."),
        ("STEP 2: IMPUTE Missing Values", "Median for numerical (LoanAmount, Loan_Amount_Term). Mode for categorical features."),
        ("STEP 3: ENCODE Categorical Features", "Binary: Gender, Married, Education, Self_Employed. Ordinal: Dependents (3+→3), Property_Area (0/1/2). Target: Y=1, N=0."),
        ("STEP 4: SCALE & SPLIT", "StandardScaler on all 11 predictors. 80/20 train-test split, random_state=42."),
    ]
    for i, (h, b) in enumerate(steps):
        top = PI(1.55 + i * 1.45)
        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PI(0.8), top, PI(11.7), PI(1.2))
        box.fill.solid(); box.fill.fore_color.rgb = LRED; box.line.color.rgb = RED
        tf = box.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = h; p.font.bold, p.font.color.rgb, p.font.size = True, RED, PPt(13)
        pb = tf.add_paragraph(); pb.text = b; pb.font.size, pb.font.color.rgb = PPt(12), GRAY

    # SLIDE 5 — Phase 2: EDA
    s5 = prs.slides.add_slide(blank)
    header(s5, "Phase 2 — Exploratory Data Analysis (EDA)")
    insights = [
        ("CREDIT HISTORY", "Strongest binary predictor — Credit_History=1 correlates with >80% approval rate."),
        ("PROPERTY AREA", "Semiurban > Urban > Rural in approval rates. Captures regional economic risk exposure."),
        ("APPLICANT INCOME", "Moderate positive correlation with approval. Income alone is not decisive."),
        ("LOAN AMOUNT (Right-Skewed)", "Validates median imputation strategy — mean would overestimate typical loan sizes."),
    ]
    for i, (h, b) in enumerate(insights):
        top = PI(1.55 + i * 1.45)
        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PI(0.8), top, PI(11.7), PI(1.2))
        box.fill.solid(); box.fill.fore_color.rgb = LRED; box.line.color.rgb = RED
        tf = box.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = h; p.font.bold, p.font.color.rgb, p.font.size = True, RED, PPt(13)
        pb = tf.add_paragraph(); pb.text = b; pb.font.size, pb.font.color.rgb = PPt(12), GRAY

    # SLIDE 6 — Phase 3 & 4: Model Comparison
    s6 = prs.slides.add_slide(blank)
    header(s6, "Phase 3 & 4 — Model Benchmark Comparison")
    t = s6.shapes.add_table(4, 6, PI(0.8), PI(1.8), PI(11.7), PI(3.6)).table
    for i, h in enumerate(["Model Algorithm", "Accuracy", "Precision", "Recall", "F1-Score", "Confusion Matrix"]):
        c = t.cell(0, i); c.text = h
        c.fill.solid(); c.fill.fore_color.rgb = RED
        p = c.text_frame.paragraphs[0]
        p.font.bold, p.font.color.rgb, p.alignment = True, WHITE, PP_ALIGN.CENTER
    rows = [
        ("Logistic Regression (Chosen)", "78.86%", "75.96%", "98.75%", "85.87%", "[[18,25],[1,79]]"),
        ("Decision Tree Classifier",     "74.80%", "75.26%", "91.25%", "82.49%", "[[19,24],[7,73]]"),
        ("Random Forest Classifier",     "77.24%", "75.49%", "96.25%", "84.62%", "[[18,25],[3,77]]"),
    ]
    for ri, row in enumerate(rows, 1):
        for ci, val in enumerate(row):
            c = t.cell(ri, ci); c.text = val
            p = c.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if ci > 0 else PP_ALIGN.LEFT
            if ri == 1:
                c.fill.solid(); c.fill.fore_color.rgb = LRED; p.font.bold = True

    # SLIDE 7 — Confusion Matrix Deep Dive
    s7 = prs.slides.add_slide(blank)
    header(s7, "Confusion Matrix Analysis — Why Recall Matters")
    cards7 = [
        ("TRUE POSITIVES: 79", "79 actual repayers correctly predicted → Loan approved. Bank earns interest."),
        ("FALSE NEGATIVES: 1", "Only 1 defaulter missed — near-zero NPA risk from the model."),
        ("FALSE POSITIVES: 25", "25 good applicants denied — revenue loss but bank fully protected."),
        ("TRUE NEGATIVES: 18", "18 defaulters correctly denied → NPA prevented."),
    ]
    for i, (h, b) in enumerate(cards7):
        top = PI(1.6 + (i // 2) * 2.6)
        left = PI(0.8 + (i % 2) * 6.0)
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, PI(5.6), PI(2.3))
        card.fill.solid(); card.fill.fore_color.rgb = LRED; card.line.color.rgb = RED
        tf = card.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = h; p.font.bold, p.font.color.rgb, p.font.size = True, RED, PPt(14)
        pb = tf.add_paragraph(); pb.text = b; pb.font.size, pb.font.color.rgb = PPt(12), GRAY
        pb.space_before = PPt(10)

    # SLIDE 8 — Streamlit UI (NEW)
    s8 = prs.slides.add_slide(blank)
    header(s8, "Streamlit Interactive Web UI (app.py)")
    left_box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PI(0.8), PI(1.6), PI(5.8), PI(5.2))
    left_box.fill.solid(); left_box.fill.fore_color.rgb = LRED; left_box.line.color.rgb = RED
    tf = left_box.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "INPUT FORM"; p.font.bold, p.font.color.rgb, p.font.size = True, RED, PPt(14)
    for item in ["Gender, Married, Dependents (dropdowns)",
                 "Education, Self_Employed (dropdowns)",
                 "ApplicantIncome, CoapplicantIncome (number inputs)",
                 "LoanAmount, Loan_Amount_Term, Credit_History",
                 "Property_Area (Rural / Semiurban / Urban)"]:
        pb = tf.add_paragraph(); pb.text = "• " + item
        pb.font.size, pb.font.color.rgb = PPt(12), GRAY; pb.space_before = PPt(7)

    right_box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PI(6.9), PI(1.6), PI(5.6), PI(5.2))
    right_box.fill.solid(); right_box.fill.fore_color.rgb = LRED; right_box.line.color.rgb = RED
    tf2 = right_box.text_frame; tf2.word_wrap = True
    p = tf2.paragraphs[0]; p.text = "OUTPUT PANEL"; p.font.bold, p.font.color.rgb, p.font.size = True, RED, PPt(14)
    for item in ["Color-coded result card (Repaid / Default Risk)",
                 "Repayment Probability progress bar (0–100%)",
                 "Default Probability progress bar (0–100%)",
                 "Tier 1 (Low) / Tier 2 (Moderate) / Tier 3 (High) risk badge",
                 "Raw probability expander for audit logs",
                 "Run: streamlit run app.py"]:
        pb = tf2.add_paragraph(); pb.text = "• " + item
        pb.font.size, pb.font.color.rgb = PPt(12), GRAY; pb.space_before = PPt(7)

    # SLIDE 9 — Business Recommendations
    s9 = prs.slides.add_slide(blank)
    header(s9, "Business Recommendations & Risk Policy")
    recs = [
        ("MAXIMIZE RECALL", "In default prediction, missing a defaulter is far more costly — prioritize high-recall models over pure accuracy."),
        ("CREDIT HISTORY ENFORCEMENT", "Mandate credit documentation for all applicants — 50 missing entries (8.1%) create dangerous scoring blind spots."),
        ("SEMIURBAN INCENTIVES", "Semiurban applicants have the highest repayment rates — offer preferential interest rate tiers for this segment."),
        ("DEPLOY STREAMLIT UI", "Roll out app.py on Streamlit Cloud or corporate intranet for branch-level officer access to instant default risk scores."),
    ]
    for i, (h, b) in enumerate(recs):
        top = PI(1.6 + i * 1.42)
        box = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PI(0.8), top, PI(11.7), PI(1.15))
        box.fill.solid(); box.fill.fore_color.rgb = LRED; box.line.color.rgb = RED
        tf = box.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = h; p.font.bold, p.font.color.rgb, p.font.size = True, RED, PPt(13)
        pb = tf.add_paragraph(); pb.text = b; pb.font.size, pb.font.color.rgb = PPt(12), GRAY

    prs.save(PPTX_OUT)
    print(f"Saved: {PPTX_OUT}")


if __name__ == "__main__":
    build_docx()
    build_pptx()
    print("\nProject 2 documents generated successfully.")
