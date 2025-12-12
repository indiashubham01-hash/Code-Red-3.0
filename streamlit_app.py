import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:8004")

# Set Page Config
st.set_page_config(page_title="MedAssist AI Dashboard", layout="wide", page_icon="🏥")

# Custom CSS
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main-header {
        font-size: 2.5rem;
        color: #4F8BF9;
    }
    .stButton>button {
        width: 100%;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏥 MedAssist AI Dashboard")
st.markdown(f"**Backend Status**: Connecting to `{API_URL}`...")

# Check Health
try:
    health = requests.get(f"{API_URL}/health")
    if health.status_code == 200:
        st.success("✅ Backend Online")
    else:
        st.error("❌ Backend Issues")
except:
    st.error(f"❌ Could not connect to {API_URL}. Ensure server is running.")

# Tabs for Models
tabs = st.tabs(["❤️ Cardiovascular", "🩸 Diabetes", "🫁 Pulmonary (IPF)", "💉 CBC Analysis", "🗣️ Medical AI Chat"])

# --- 1. Cardiovascular ---
with tabs[0]:
    st.header("Cardiovascular Disease Risk")
    col1, col2 = st.columns(2)
    with col1:
        age_years = st.number_input("Age (Years)", 20, 100, 50)
        gender = st.selectbox("Gender", options=[1, 2], format_func=lambda x: "Female" if x==1 else "Male")
        height = st.number_input("Height (cm)", 100, 250, 170)
        weight = st.number_input("Weight (kg)", 30, 200, 70)
        ap_hi = st.number_input("Systolic BP (ap_hi)", 50, 250, 120)
        ap_lo = st.number_input("Diastolic BP (ap_lo)", 30, 200, 80)
    with col2:
        cholesterol = st.selectbox("Cholesterol", [1, 2, 3], format_func=lambda x: {1: "Normal", 2: "Above Normal", 3: "High"}[x])
        gluc = st.selectbox("Glucose", [1, 2, 3], format_func=lambda x: {1: "Normal", 2: "Above Normal", 3: "High"}[x])
        smoke = st.selectbox("Smoking", [0, 1], format_func=lambda x: "No" if x==0 else "Yes")
        alco = st.selectbox("Alcohol", [0, 1], format_func=lambda x: "No" if x==0 else "Yes")
        active = st.selectbox("Physical Activity", [0, 1], format_func=lambda x: "No" if x==0 else "Yes")

    if st.button("Predict Cardio Risk", type="primary"):
        # Convert Age to days roughly
        age_days = age_years * 365
        payload = {
            "age": int(age_days), "gender": gender, "height": height, "weight": weight,
            "ap_hi": ap_hi, "ap_lo": ap_lo, "cholesterol": cholesterol, "gluc": gluc,
            "smoke": smoke, "alco": alco, "active": active
        }
        try:
            res = requests.post(f"{API_URL}/predict/cardiovascular", json=payload)
            if res.status_code == 200:
                data = res.json()
                st.subheader("Results")
                prob = data['risk_probability']
                
                # Gauge visualization
                st.progress(prob)
                st.metric("Risk Probability", f"{prob*100:.1f}%", delta=data.get('risk_category'))
                
                if 'explanations' in data and data['explanations']:
                    st.write("### Top Risk Factors")
                    for factor in data['explanations']['explanations'][:3]:
                        st.info(f"**{factor['feature']}**: {factor['impact']} risk (Importance: {factor['importance']:.4f})")
            else:
                st.error(f"Error: {res.text}")
        except Exception as e:
            st.error(f"Connection Error: {e}")

# --- 2. Diabetes ---
with tabs[1]:
    st.header("Diabetes Risk Prediction")
    c1, c2 = st.columns(2)
    with c1:
        d_age = st.number_input("Age", 0, 120, 45, key="d_age")
        d_gender = st.selectbox("Gender", ["Male", "Female"], key="d_gen")
        d_hyper = st.selectbox("Hypertension", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
        d_heart = st.selectbox("Heart Disease", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
    with c2:
        d_smoke = st.selectbox("Smoking History", ["never", "current", "former", "ever", "not current", "No Info"])
        d_bmi = st.number_input("BMI", 10.0, 60.0, 25.0)
        d_hba1c = st.number_input("HbA1c Level", 3.0, 15.0, 5.5)
        d_gluc = st.number_input("Blood Glucose", 50, 400, 100)

    if st.button("Predict Diabetes", type="primary"):
        payload = {
            "age": d_age, "gender": d_gender, "hypertension": d_hyper, "heart_disease": d_heart,
            "smoking_history": d_smoke, "bmi": d_bmi, "HbA1c_level": d_hba1c, "blood_glucose_level": int(d_gluc)
        }
        try:
            res = requests.post(f"{API_URL}/predict/diabetes", json=payload)
            if res.status_code == 200:
                data = res.json()
                st.metric("Diabetes Risk", f"{data['risk_probability']*100:.1f}%", data['risk_category'])
                st.progress(data['risk_probability'])
            else: st.error(res.text)
        except Exception as e: st.error(e)

# --- 3. Idiopathic (IPF) ---
with tabs[2]:
    st.header("Idiopathic Pulmonary Fibrosis Prediction")
    i_age = st.slider("Age", 20, 100, 65)
    i_gender = st.selectbox("Gender", ["Male", "Female"], key="i_gen")
    i_smoke = st.radio("Smoking History", ["Ever", "Never"], key="i_smoke")
    
    if st.button("Analyze IPF Risk"):
        payload = {"age": i_age, "gender": i_gender, "smoking_history": i_smoke}
        try:
            res = requests.post(f"{API_URL}/predict/idiopathic", json=payload)
            if res.status_code == 200:
                data = res.json()
                res_col1, res_col2 = st.columns(2)
                res_col1.metric("Prediction", data['prediction'])
                res_col2.metric("Probability", f"{data['risk_probability']:.4f}")
                
                if data['prediction'] == "IPF":
                    st.warning("High likelihood of Idiopathic Pulmonary Fibrosis.")
                else:
                    st.success("Normal profile.")
            else: st.error(res.text)
        except Exception as e: st.error(e)

# --- 4. CBC ---
with tabs[3]:
    st.header("CBC Blood Work Analysis")
    cbc_sex = st.selectbox("Sex", ["male", "female"], key="cbc_sex")
    c_wbc = st.number_input("WBC (x10^9/L)", 0.0, 50.0, 8.5)
    c_rbc = st.number_input("RBC", 0.0, 10.0, 4.8)
    c_hb = st.number_input("Hemoglobin", 0.0, 25.0, 14.0)
    c_hct = st.number_input("Hematocrit (%)", 0.0, 100.0, 42.0)
    c_plt = st.number_input("Platelets", 0.0, 1000.0, 250.0)

    if st.button("Analyze Report"):
        payload = {
            "sex": cbc_sex, "wbc": c_wbc, "rbc": c_rbc, "hemoglobin": c_hb,
            "hematocrit": c_hct, "platelets": c_plt
        }
        try:
            res = requests.post(f"{API_URL}/analyze_cbc", json=payload)
            if res.status_code == 200:
                data = res.json()
                st.write(f"**Summary**: {data['summary']}")
                st.json(data['findings'])
            else: st.error(res.text)
        except Exception as e: st.error(e)

# --- 5. Medical Graph/Chat ---
with tabs[4]:
    st.header("Medical AI Assistant")
    
    mode = st.radio("Mode", ["Medical Chat", "Text Analysis (ClinicalBERT)"])
    
    if mode == "Medical Chat":
        st.info("Powered by Meditron-7b via Ollama")
        user_input = st.text_input("Ask a medical question:")
        if st.button("Send"):
            try:
                with st.spinner("Thinking..."):
                    res = requests.post(f"{API_URL}/chat/meditron", json={"message": user_input, "history": []})
                    if res.status_code == 200:
                        st.markdown(f"**AI**: {res.json()['response']}")
                    else: st.error("Chat service unavailable. Ensure backend has Ollama running.")
            except Exception as e: st.error(e)

    else:
        st.info("Masked Language Modeling (ClinicalBERT)")
        text_input = st.text_area("Enter sentence with [MASK]", "The patient was prescribed [MASK] for hypertension.")
        if st.button("Analyze"):
            try:
                res = requests.post(f"{API_URL}/analyze/clinical_bert", json={"text": text_input})
                if res.status_code == 200:
                    st.write(res.json())
                else: st.error(res.text)
            except Exception as e: st.error(e)
