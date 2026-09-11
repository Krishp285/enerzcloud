# Dual-Project Credit Risk Portfolio: Loan Approval & Loan Default Prediction

A dual-project machine learning portfolio providing automated credit risk evaluation, continuous approval probability scoring, and a 4-phase default prediction classification pipeline.

---

## 📁 Repository Directory Structure

```
enerzcloud/
│
├── project/loan_approval_fullstack-main/   # PROJECT 1: LOAN APPROVAL SYSTEM
│   ├── backend/
│   │   ├── app.py                         # FastAPI REST server serving predictions & probabilities
│   │   ├── model.pkl                      # Trained Random Forest Classifier artifact
│   │   ├── scaler.pkl                     # Trained StandardScaler artifact
│   │   └── metrics.json                   # Serialized metrics JSON
│   ├── frontend/
│   │   └── streamlit_app.py               # Streamlit interactive UI dashboard
│   ├── loan_approval_dataset.csv          # Primary dataset (4,269 customer records)
│   ├── loan.py                            # Project 1 pipeline script
│   ├── Dual_Project_Loan_Prediction_Report.docx       # Dual-Project Word Report (.docx)
│   ├── Dual_Project_Loan_Prediction_Presentation.pptx # Widescreen PowerPoint Pitch Deck (.pptx)
│   └── generate_dual_docs.py              # Document generator script
│
└── day-19/                                 # PROJECT 2: LOAN DEFAULT SYSTEM
    ├── task.py                            # 4-Phase ML pipeline on loan-data.csv
    ├── eda_plots.png                      # Distribution & count plots
    ├── correlation_heatmap.png            # Correlation matrix heatmap
    └── model_comparison.png               # Benchmark accuracy & metrics bar plot
```

---

## 📄 Key Portfolio Deliverables
- 📝 **Dual-Project Word Report**: [Dual_Project_Loan_Prediction_Report.docx](file:///c:/Users/DELL/OneDrive/Desktop/enerzcloud/project/loan_approval_fullstack-main/Dual_Project_Loan_Prediction_Report.docx)
- 📊 **PowerPoint Pitch Deck**: [Dual_Project_Loan_Prediction_Presentation.pptx](file:///c:/Users/DELL/OneDrive/Desktop/enerzcloud/project/loan_approval_fullstack-main/Dual_Project_Loan_Prediction_Presentation.pptx)
- 🐍 **Project 1 Pipeline (Loan Approval)**: [loan.py](file:///c:/Users/DELL/OneDrive/Desktop/enerzcloud/project/loan_approval_fullstack-main/loan.py)
- 🐍 **Project 2 Pipeline (Loan Default)**: [task.py](file:///c:/Users/DELL/OneDrive/Desktop/enerzcloud/day-19/task.py)

---

## 📊 Performance Comparison Summary

### Project 1: Loan Approval Prediction (4,269 Records)
| Model Algorithm | Accuracy | Precision | Recall | F1-Score | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 90.75% | 92.24% | 93.10% | 92.66% | Baseline |
| **Decision Tree** | 97.89% | 97.26% | 99.44% | 98.34% | High Accuracy |
| **Random Forest (Chosen)** | **97.89%** | **97.61%** | **99.07%** | **98.33%** | **Production Deployed** |

### Project 2: Loan Default Prediction (614 Records)
| Model Algorithm | Accuracy | Precision | Recall | F1-Score | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Chosen)** | **78.86%** | **75.96%** | **98.75%** | **85.87%** | **Top Performer** |
| **Random Forest** | 77.24% | 75.49% | 96.25% | 84.62% | Competitive |
| **Decision Tree** | 74.80% | 75.26% | 91.25% | 82.49% | Baseline |

---

## 🚀 Execution Instructions

### Project 1: Run Fullstack Application
1. **Train Model Pipeline**:
   ```bash
   python project/loan_approval_fullstack-main/loan.py
   ```
2. **Start FastAPI Backend**:
   ```bash
   uvicorn backend.app:app --reload --port 8000
   ```
3. **Start Streamlit Web UI**:
   ```bash
   streamlit run frontend/streamlit_app.py
   ```

### Project 2: Run 4-Phase Classification Pipeline
```bash
python day-19/task.py
```

### Regenerate Word & PowerPoint Files
```bash
python project/loan_approval_fullstack-main/generate_dual_docs.py
```
