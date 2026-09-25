# AI-Powered Financial Fraud Detection System

> A multi-factor, explainable financial risk surveillance system integrating supervised machine learning, deterministic rule engines, user behavioural anomaly profiling, velocity tracking, and SQLite persistence behind a Streamlit dashboard.

---

## 1. Project Overview
Financial fraud represents one of the fastest-growing threats across global banking and digital payment ecosystems. Conventional solutions often rely either solely on rigid rules (which fraudsters easily evade) or opaque machine learning models (which suffer from high false-alarm rates and lack regulatory explainability).

The **AI-Powered Financial Fraud Detection System** bridges this gap by unifying **Machine Learning (SMOTE-balanced)**, **Deterministic Rules**, **User Behavioural Profiling**, and **Burst Velocity Analytics** into a consolidated, transparent **Composite Risk Scoring Engine (0–100)**. Every classified transaction includes specific, human-readable **Explainable AI (XAI)** decision reasons.

---

## 2. Problem Statement
- **Extreme Class Imbalance:** Legitimate transactions outnumber fraudulent events by more than 500 to 1 (<0.2% fraud), rendering raw accuracy misleading.
- **Dynamic Fraud Vectors:** Fraudsters continually adapt spending velocity, amounts, and geographic locations to bypass static thresholds.
- **The Black-Box Problem:** Black-box classifiers provide probabilities without audit trails, frustrating customers and violating financial compliance mandates.
- **Siloed Systems:** Banking operations frequently separate rule filters from ML scoring, creating operational delays and fragmented telemetry.

---

## 3. Objectives
1. Build an end-to-end Python 3.12+ application that runs locally on Windows without cloud dependencies.
2. Implement stratified data cleaning, feature engineering, and training-only SMOTE oversampling.
3. Train, benchmark, and compare multiple classifiers: **Logistic Regression**, **Decision Tree**, and **Random Forest** (optimizing for Recall, Precision, and F1).
4. Engineer multi-engine risk evaluation:
   $$\text{Final Risk Score} = (P_{\text{ML}} \times 100 \times 0.50) + (S_{\text{Rule}} \times 0.20) + (S_{\text{Beh}} \times 0.20) + (S_{\text{Vel}} \times 0.10)$$
5. Provide actionable, human-readable decision explanations for every flagged transaction.
6. Provide role-based authentication with bcrypt password security and SQLite persistence.
7. Deliver an interactive Streamlit dashboard with KPI metrics, Plotly distribution charts, and ledger search.

---

## 4. Key Features
- **Multi-Factor Risk Scoring:** Composite 0–100 score mapping to **LEGITIMATE** (Approve), **SUSPICIOUS** (Verify), and **FRAUD** (Block).
- **Explainable AI (XAI):** Clear rationale articulating why amounts, hours, velocity, or devices triggered elevated risk.
- **Interactive Simulator:** Live transaction scoring with instant presets for Legitimate, Suspicious, and Critical Fraud scenarios.
- **Executive Dashboard:** Plotly charts showing fraud prevalence, risk score histograms, hourly threat distributions, and ticket size spreads.
- **Model Governance:** Precision-Recall curves, ROC curves, confusion matrix heatmaps, and architecture leaderboards.
- **Searchable Audit Ledger:** Complete transaction history with classification filters, customer search, and one-click CSV export.
- **Security & RBAC:** Salted bcrypt password hashing and session-protected administrative pages.

---

## 5. Architecture
```
                         ┌───────────────────────────────────┐
                         │   Incoming Transaction Payload    │
                         └─────────────────┬─────────────────┘
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    ▼                                             ▼
       ┌───────────────────────────┐                ┌───────────────────────────┐
       │   Feature Engineering     │                │   User Profile & Ledger   │
       │ (log_amount, hour, night) │                │  (History, Avg, Devices)  │
       └────────────┬──────────────┘                └─────────────┬─────────────┘
                    ▼                                             ▼
       ┌───────────────────────────┐                ┌───────────────────────────┐
       │   StandardScaler Scale    │                │  Deterministic Rule Engine│
       └────────────┬──────────────┘                │ (Limits, Night, Repetition)│
                    ▼                               └─────────────┬─────────────┘
       ┌───────────────────────────┐                              │
       │   ML Champion Classifier  │                              ▼
       │  (Random Forest / SMOTE)  │                ┌───────────────────────────┐
       └────────────┬──────────────┘                │  User Behaviour Profiling │
                    │                               │   (Spend, Device, Geo)    │
                    │                               └─────────────┬─────────────┘
                    │                                             ▼
                    │                               ┌───────────────────────────┐
                    │                               │  Burst Velocity Engine    │
                    │                               │   (5m, 30m, 1h Rolling)   │
                    │                               └─────────────┬─────────────┘
                    ▼                                             ▼
       ┌────────────────────────────────────────────────────────────────────────┐
       │              Composite Risk Engine & Classification Mapping             │
       │               (0-30: Legit | 31-70: Suspicious | 71-100: Fraud)        │
       └───────────────────────────────────┬────────────────────────────────────┘
                                           ▼
       ┌────────────────────────────────────────────────────────────────────────┐
       │                 Explainable AI (XAI) Reason Synthesis                  │
       └───────────────────────────────────┬────────────────────────────────────┘
                                           ▼
       ┌────────────────────────────────────────────────────────────────────────┐
       │             Persistence (SQLite) & Streamlit UI Rendering             │
       └────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Technology Stack
| Category | Technology | Purpose |
|---|---|---|
| **Runtime** | Python 3.12+ | Core execution environment |
| **Frontend** | Streamlit | Web dashboard, real-time forms, navigation |
| **Backend Architecture** | Modular Python OOP | Decoupled engines and clean separation of concerns |
| **Database** | SQLite3 (WAL Mode) | Local relational persistence, indexed queries |
| **Data Processing** | Pandas, NumPy | Data cleaning, reshaping, and feature calculation |
| **Machine Learning** | Scikit-learn, Imblearn | Classifiers, StandardScaler, stratified split, SMOTE |
| **Visualizations** | Plotly | Dynamic, interactive charts and histograms |
| **Security** | bcrypt | Salted password hashing |
| **Testing** | pytest | Automated unit and integration test suite |

---

## 7. Dataset
The system supports two complementary dataset modes:
1. **Real-World Kaggle Dataset:**
   - Standard Credit Card Fraud Detection benchmark (ULB).
   - Features: `Time`, `V1` through `V28` (PCA transformed), `Amount`, `Class` (0 = Legitimate, 1 = Fraud).
   - Place in: `data/raw/creditcard.csv`.
2. **Realistic Synthetic Demonstration Dataset:**
   - Generated via `python scripts/generate_demo_data.py`.
   - Produces 6,000 multi-dimensional records matching Kaggle schema, alongside enriched customer IDs, geolocations, devices, and merchants.
   - Saved to: `data/processed/demo_creditcard.csv`.
   - *Note: Clearly labeled as DEMO DATA for academic demonstration.*

---

## 8. Machine Learning Methodology
1. **Stratified Split:** 80% train / 20% test partition preserving true class proportions.
2. **Feature Standardization:** `StandardScaler` fitted **only** on the training split to avoid data leakage.
3. **Training-Only SMOTE:** Synthetic Minority Over-sampling applied exclusively to `X_train`, leaving `X_test` untouched to reflect natural distribution.
4. **Architectures Evaluated:**
   - **Logistic Regression:** Linear baseline with class weighting.
   - **Decision Tree:** Interpretable tree with depth regularization.
   - **Random Forest:** Ensemble of bagging trees mitigating variance.
   - **XGBoost (Optional):** Gradient boosting if installed.
5. **Selection Metric:** Champion model chosen via **F1 Score** and **PR-AUC** rather than misleading raw accuracy.

---

## 9. Risk Scoring Formula
$$\text{Final Risk Score} = (P_{\text{ML}} \times 100 \times w_{\text{ML}}) + (S_{\text{Rule}} \times w_{\text{Rule}}) + (S_{\text{Beh}} \times w_{\text{Beh}}) + (S_{\text{Vel}} \times w_{\text{Vel}})$$

- **Default Weights:**
  - $w_{\text{ML}} = 0.50$ (50%)
  - $w_{\text{Rule}} = 0.20$ (20%)
  - $w_{\text{Beh}} = 0.20$ (20%)
  - $w_{\text{Vel}} = 0.10$ (10%)
- **Classification Boundaries:**
  - `0 – 30`: **LEGITIMATE** $\rightarrow$ Action: `APPROVE`
  - `31 – 70`: **SUSPICIOUS** $\rightarrow$ Action: `VERIFY / MANUAL REVIEW`
  - `71 – 100`: **FRAUD** $\rightarrow$ Action: `BLOCK`

---

## 10. Database Schema
SQLite database stored at `database/fraud_detection.db`:
- **`users`**: User identity, email, salted bcrypt password hash, role (`analyst`, `auditor`, `admin`).
- **`transactions`**: Transaction ID, customer ID, amount, timestamp, device, location, merchant, ML probability, component scores, final risk, verdict, action, and JSON reasons.
- **`fraud_rules`**: Heuristic rules, descriptions, weights, active status.
- **`user_profiles`**: Historical spend averages, maximums, typical active hours, trusted devices, familiar cities.
- **`prediction_logs`**: Immutable audit logs of all risk assessments.
- **`application_logs`**: System operational logs.

---

## 11. Project Directory Structure
```
Finance-Fraud-Detection/
│
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
│
├── config/
│   ├── __init__.py
│   └── settings.py             # Centralized settings and paths
│
├── database/
│   ├── __init__.py
│   ├── connection.py           # SQLite connection manager (WAL mode)
│   ├── schema.py               # Table creation & rule seeding
│   └── crud.py                 # Parameterized database operations
│
├── authentication/
│   ├── __init__.py
│   ├── auth.py                 # Registration & session state management
│   └── password.py             # bcrypt hashing & verification
│
├── preprocessing/
│   ├── __init__.py
│   ├── data_loader.py          # Real & demo dataset loader
│   ├── cleaner.py              # Missing, duplicate & outlier analysis
│   ├── feature_engineering.py  # Temporal & log feature engineering
│   └── pipeline.py             # Split, scaling, and SMOTE pipeline
│
├── models/
│   ├── __init__.py
│   ├── model_manager.py        # Artifact loading & safe inference
│   ├── trainer.py              # Multi-model training orchestrator
│   └── evaluator.py            # Precision, Recall, F1, ROC/PR curves
│
├── fraud_detection/
│   ├── __init__.py
│   ├── rule_engine.py          # Deterministic heuristic rules
│   ├── behaviour_engine.py     # User baseline deviation scoring
│   ├── velocity_engine.py      # Rolling frequency burst scoring
│   ├── risk_engine.py          # Multi-factor composite risk formula
│   ├── explanation_engine.py   # Explainable AI (XAI) reason generator
│   └── prediction_engine.py    # Main lifecycle orchestrator
│
├── dashboard/
│   ├── __init__.py
│   ├── components.py           # Cards, banners, CSS styles
│   ├── charts.py               # Robust Plotly interactive charts
│   └── metrics.py              # Aggregation functions
│
├── pages/
│   ├── home.py                 # Overview & architecture workflow
│   ├── login.py                # Security analyst login
│   ├── signup.py               # New operator registration
│   ├── dashboard.py            # KPI metrics & distribution plots
│   ├── fraud_detection.py      # Live interactive risk simulator
│   ├── transaction_history.py  # Ledger search, detail view & CSV export
│   ├── analytics.py            # Merchant & geographic threat slicing
│   ├── model_performance.py    # ROC/PR curves, confusion matrix, benchmark
│   ├── settings.py             # Dynamic threshold & weight tuning
│   └── about.py                # Academic disclosures & tech stack
│
├── scripts/
│   ├── initialize_database.py  # DB table creation & seeding
│   ├── generate_demo_data.py   # 6,000 synthetic records & user cohort
│   ├── train_model.py          # End-to-end ML training pipeline
│   └── run_pipeline.py         # Master all-in-one setup runner
│
├── data/
│   ├── raw/                    # Location for creditcard.csv
│   └── processed/              # Generated demo datasets
│
├── artifacts/
│   ├── models/                 # Saved model, metrics, and metadata
│   └── preprocessing/          # Saved StandardScaler & feature names
│
├── tests/
│   ├── test_auth.py            # Authentication & bcrypt tests
│   ├── test_rules.py           # Rule engine unit tests
│   ├── test_risk.py            # Risk formula & threshold tests
│   ├── test_prediction.py      # Prediction pipeline integration tests
│   └── test_database.py        # SQLite CRUD tests
│
└── docs/
    └── PROJECT_DOCUMENTATION.md # Comprehensive 31-chapter academic report
```

---

## 12. Quickstart Installation & Execution

### Step 1: Open PowerShell / Terminal
```bash
cd Finance-Fraud-Detection
```

### Step 2: Create & Activate Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
python scripts/initialize_database.py
```

### Step 5: Generate Demo Dataset (6,000 records)
```bash
python scripts/generate_demo_data.py
```

### Step 6: Train Machine Learning Models
```bash
python scripts/train_model.py
```

### Step 7: Run Automated Unit Tests
```bash
python -m pytest
```

### Step 8: Launch Interactive Dashboard
```bash
python -m streamlit run app.py
```

---

## 13. Default Demonstration Credentials
| Attribute | Value |
|---|---|
| **Username** | `demo_analyst` |
| **Password** | `Demo@12345` |
| **Designation** | `Admin / Senior Fraud Analyst` |

---

## 14. Academic & Engineering Disclaimers
1. **Academic Demonstration:** This system is built for college projects, engineering demonstrations, viva defense, and portfolio review. It is not approved for live financial gateway clearing.
2. **Kaggle Anonymity:** Public fraud datasets anonymize features via PCA (`V1` to `V28`). Enriched fields (`user_id`, `device_id`, `location`, `merchant`) are generated as demonstration layers.
3. **Database Architecture:** SQLite is utilized for self-contained local demonstration without requiring external database servers.

---

## 15. License
MIT License. Free for educational, academic, and portfolio use.
