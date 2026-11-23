import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.set_page_config(page_title="FundScope", layout="centered")

st.title("🏦 FundScope")
st.write("""
This prototype application assists loan officers in analyzing applicant default risks.
It utilizes our trained **Random Forest** pipeline to provide automated predictions, risk category explanations,
and key recommendations.
""")

@st.cache_resource
def load_pipeline():
    try:
        return joblib.load('rf_pipeline_engineered.pkl')
    except Exception as e:
        st.warning("Engineered RF pipeline not found. Falling back to Baseline RF pipeline.")
        return joblib.load('rf_pipeline_baseline.pkl')

pipeline = load_pipeline()

st.subheader("📋 Applicant Information Form")
with st.form("credit_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        income = st.number_input("Annual Income ($)", min_value=1000, max_value=10000000, value=50000, step=1000)
        age = st.number_input("Applicant Age", min_value=18, max_value=100, value=30, step=1)
        experience = st.number_input("Total Professional Experience (Years)", min_value=0, max_value=50, value=5, step=1)
        current_job_yrs = st.number_input("Years at Current Job", min_value=0, max_value=30, value=2, step=1)
        current_house_yrs = st.number_input("Years in Current House", min_value=10, max_value=14, value=12, step=1)
        
    with col2:
        married_single = st.selectbox("Marital Status", ["single", "married"])
        house_ownership = st.selectbox("Housing Status", ["rented", "owned", "norent_noowned"])
        car_ownership = st.selectbox("Car Ownership", ["no", "yes"])
        profession = st.selectbox("Profession", ['Mechanical_engineer', 'Software_Developer', 'Technical_writer', 'Civil_servant', 'Physician', 'Other'])
        city = st.text_input("City (e.g. Rewa, Parbhani, New_Delhi)", "Rewa")
        state = st.text_input("State (e.g. Madhya_Pradesh, Maharashtra, Delhi)", "Madhya_Pradesh")
        
    submit = st.form_submit_button("Run Risk Assessment")

if submit:
    input_data = pd.DataFrame([{
        'Income': income,
        'Age': age,
        'Experience': experience,
        'Married/Single': married_single,
        'House_Ownership': house_ownership,
        'Car_Ownership': car_ownership,
        'Profession': profession,
        'CITY': city,
        'STATE': state,
        'CURRENT_JOB_YRS': current_job_yrs,
        'CURRENT_HOUSE_YRS': float(current_house_yrs)
    }])
    
    try:
        input_data['Income_per_Tenure'] = input_data['Income'] / (input_data['CURRENT_JOB_YRS'] + 1)
        adjusted_age = input_data['Age'].clip(lower=19)
        input_data['Experience_to_Age_Ratio'] = input_data['Experience'] / (adjusted_age - 18)
        prob = pipeline.predict_proba(input_data)[0][1]
        pred_class = pipeline.predict(input_data)[0]
        
        st.subheader("📊 Risk Analysis Report")
        col_left, col_right = st.columns([1, 2])
        
        with col_left:
            st.metric(label="Default Probability", value=f"{prob * 100:.2f}%")
            
        with col_right:
            if prob < 0.35:
                st.success("🟢 LOW RISK: Approved for automated processing.")
            elif prob < 0.65:
                st.warning("🟡 MEDIUM RISK: Manual evaluation recommended.")
            else:
                st.error("🔴 HIGH RISK: Referral to senior credit committee.")
                
        st.write(f"**Decision-Support Context:** Under current class-balanced settings (default baseline ~12.4%), this applicant is assigned a risk factor score of **{prob:.4f}**. Underwriters should cross-reference this score with external local banking history parameters before taking absolute actions.")
        
    except Exception as err:
        st.error(f"An error occurred while evaluating the application: {err}")
