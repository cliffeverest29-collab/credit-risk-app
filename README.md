# credit-risk-app (FundScope)

**FundScope** is an interactive Streamlit credit risk decision-support prototype designed to assist loan officers in evaluating borrower default risk. It loads a trained **Random Forest** pipeline (`rf_pipeline_engineered.pkl`, with fallback to `rf_pipeline_baseline.pkl`), computes engineered tenure/experience ratios, estimates default probability, and assigns actionable risk tiers.

**Live Deployment:** `(https://credit-risk-app-m4deudswt7sjmnkejz9ufu.streamlit.app/)`

## Data Origin and Licence

- **Source / Origin:** ('/content/CSE bank data project 1.csv')
- **Data Licence & Terms:** `(CC0 1.0, All rights reserved`)
**Code Licence:** All rights reserved (no open-source license added yet).

## Target Definition

- **Target Column:** Risk_Flag 
- **Positive Class (`1` = Default / High Risk):** ``
- **Negative Class (`0` = Non-Default / Low Risk):** 
- **Baseline & Exclusions:** Observed baseline default rate of roughly **12.4%** in `app.py`

## Required Libraries

From `requirements.txt`:

- `streamlit>=1.20.0`
- `pandas>=1.3.0`
- `scikit-learn>=1.0.0`
- `joblib>=1.1.0`
- `numpy>=1.20.0`
- `matplotlib>=3.4.0`
- `seaborn>=0.11.0`

## Setup and Run Commands

### 1. Clone and create a virtual environment

```bash
git clone [https://github.com/cliffeverest29-collab/credit-risk-app.git](https://github.com/cliffeverest29-collab/credit-risk-app.git)
cd credit-risk-app
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
