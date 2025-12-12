from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import torch
import torch.nn as nn
import joblib
import numpy as np
import pandas as pd
import shap
import warnings
import pickle
import socket
from typing import Dict, List, Any, Optional

# NLP Imports
from transformers import pipeline
import ollama

# Import models/schemas
from model_utils import CardioNN
from schemas import CardioInput, CardioPrediction, DiabetesInput, CBCInput, IdiopathicInput, TextAnalysisInput, ChatInput

# Suppress warnings
warnings.filterwarnings('ignore')

app = FastAPI(title="MedAssist Comprehensive AI API", description="Unified API for Cardiovascular, Diabetes, CBC, IPF, and Medical NLP")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Model Classes ---
class IdiopathicNN(nn.Module):
    def __init__(self, input_dim):
        super(IdiopathicNN, self).__init__()
        self.layer1 = nn.Linear(input_dim, 16)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(16, 8)
        self.output = nn.Linear(8, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        x = self.sigmoid(self.output(x))
        return x

# --- Global Artifacts ---
artifacts = {
    "cardio_nn": {"model": None, "scaler": None},
    "cardio_xgb": {"model": None, "explainer": None},
    "diabetes_xgb": {"model": None, "encoders": None, "features": None, "explainer": None},
    "idiopathic": {"model": None, "scaler": None, "encoders": None},
    "nlp_bert": None
}

# --- Helper Functions ---
def get_risk_category(probability: float) -> str:
    if probability < 0.3: return 'Low'
    elif probability < 0.7: return 'Medium'
    else: return 'High'

def format_shap_explanation(shap_values, feature_names, feature_values):
    # (Simplified for brevity, same logic as before)
    explanations = []
    if isinstance(shap_values, list): shap_vals = shap_values[1]
    elif len(shap_values.shape) == 2: shap_vals = shap_values[0]
    else: shap_vals = shap_values
    
    feat_vals = feature_values[0] if len(feature_values.shape) > 1 else feature_values
    
    for i, (feature, shap_val, feature_val) in enumerate(zip(feature_names, shap_vals, feat_vals)):
        impact = "increases" if shap_val > 0 else "decreases"
        explanations.append({'feature': feature, 'value': float(feature_val), 'shap_value': float(shap_val), 'impact': impact, 'importance': abs(float(shap_val))})
    
    explanations.sort(key=lambda x: x['importance'], reverse=True)
    return {'explanations': explanations, 'top_factors': explanations[:5]}

# --- Startup Event ---
@app.on_event("startup")
def startup_event():
    print("Loading models...")
    
    # ... (Model loading logic is inside load_models, merging it here or keeping it separate)
    # Actually, I should just add the print logic to the existing load_models function or a new one.
    # The current code has `def load_models():`. I will modify it to print the IP.
    
    # Get Local IP
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "127.0.0.1"
    
    print("\n" + "="*50)
    print(f" SERVER RUNNING ON PORT 8004")
    print(f" Local URL:   http://127.0.0.1:8004")
    print(f" Network URL: http://{local_ip}:8004")
    print(f" Docs URL:    http://{local_ip}:8004/docs")
    print("="*50 + "\n")

    # 1. Cardio NN
    try:
        artifacts["cardio_nn"]["scaler"] = joblib.load("scaler.pkl")
        model = CardioNN(11)
        model.load_state_dict(torch.load("cardio_model.pth"))
        model.eval()
        artifacts["cardio_nn"]["model"] = model
        print("Cardio NN Loaded.")
    except Exception as e: print(f"Cardio NN Failed: {e}")

    # 2. Cardio XGB
    try:
        artifacts["cardio_xgb"]["model"] = joblib.load("xgboost_model.pkl")
        try: artifacts["cardio_xgb"]["explainer"] = shap.TreeExplainer(artifacts["cardio_xgb"]["model"])
        except: pass
        print("Cardio XGB Loaded.")
    except Exception as e: print(f"Cardio XGB Failed: {e}")

    # 3. Diabetes
    try:
        artifacts["diabetes_xgb"]["model"] = joblib.load("diabetes_xgboost_model.pkl")
        with open("diabetes_label_encoders.pkl", "rb") as f: artifacts["diabetes_xgb"]["encoders"] = pickle.load(f)
        with open("diabetes_feature_info.pkl", "rb") as f: artifacts["diabetes_xgb"]["features"] = pickle.load(f)
        try: artifacts["diabetes_xgb"]["explainer"] = shap.TreeExplainer(artifacts["diabetes_xgb"]["model"])
        except: pass
        print("Diabetes Loaded.")
    except Exception as e: print(f"Diabetes Failed: {e}")

    # 4. Idiopathic
    try:
        model_ipf = IdiopathicNN(input_dim=3)
        model_ipf.load_state_dict(torch.load("idiopathic_model.pth"))
        model_ipf.eval()
        artifacts["idiopathic"]["model"] = model_ipf
        artifacts["idiopathic"]["scaler"] = joblib.load("idiopathic_scaler.pkl")
        artifacts["idiopathic"]["encoders"] = joblib.load("idiopathic_encoders.pkl")
        print("Idiopathic Loaded.")
    except Exception as e: print(f"Idiopathic Failed: {e}")

    # 5. NLP - ClinicalBERT
    try:
        print("Loading ClinicalBERT...")
        artifacts["nlp_bert"] = pipeline("fill-mask", model="medicalai/ClinicalBERT")
        print("ClinicalBERT Loaded.")
    except Exception as e: print(f"ClinicalBERT Failed: {e}")


# --- Endpoints ---

@app.get("/health")
def health():
    return {
        "status": "online", 
        "models": {k: (v if k=='nlp_bert' else v['model']) is not None for k,v in artifacts.items()}
    }

# Cardio NN
@app.post("/predict", response_model=CardioPrediction)
def predict_original(input_data: CardioInput):
    if not artifacts["cardio_nn"]["model"]: raise HTTPException(503, "Model not loaded")
    age_years = input_data.age / 365.25
    features = np.array([[input_data.gender, input_data.height, input_data.weight, input_data.ap_hi, input_data.ap_lo, input_data.cholesterol, input_data.gluc, input_data.smoke, input_data.alco, input_data.active, age_years]])
    scaled = artifacts["cardio_nn"]["scaler"].transform(features)
    with torch.no_grad():
        prob = torch.sigmoid(artifacts["cardio_nn"]["model"](torch.FloatTensor(scaled))).item()
    return {"probability": prob, "prediction": 1 if prob > 0.5 else 0, "message": "High risk" if prob > 0.5 else "Low risk"}

# Cardio XGB
@app.post("/predict/cardiovascular")
def predict_cardio_xgb(input_data: CardioInput):
    if not artifacts["cardio_xgb"]["model"]: raise HTTPException(503, "Model not loaded")
    age_years = input_data.age / 365.25
    height_m = input_data.height / 100
    features = np.array([[age_years, input_data.gender, input_data.height, input_data.weight, input_data.ap_hi, input_data.ap_lo, input_data.cholesterol, input_data.gluc, input_data.smoke, input_data.alco, input_data.active]])
    model = artifacts["cardio_xgb"]["model"]
    prob = float(model.predict_proba(features)[0][1])
    # Explanations
    expl = None
    if artifacts["cardio_xgb"]["explainer"]:
        shap_vals = artifacts["cardio_xgb"]["explainer"].shap_values(features)
        feature_names = ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active']
        expl = format_shap_explanation(shap_vals, feature_names, features)
    return {"risk_probability": prob, "risk_category": get_risk_category(prob), "explanations": expl}

# Diabetes
@app.post("/predict/diabetes")
def predict_diabetes(input_data: DiabetesInput):
    if not artifacts["diabetes_xgb"]["model"]: raise HTTPException(503, "Model not loaded")
    encs = artifacts["diabetes_xgb"]["encoders"]
    try:
        gen = encs['gender_encoder'].transform([input_data.gender])[0]
        chk = encs['smoking_encoder'].transform([input_data.smoking_history])[0]
    except: raise HTTPException(400, "Invalid categorical input")
    features = np.array([[input_data.age, input_data.hypertension, input_data.heart_disease, input_data.bmi, input_data.HbA1c_level, input_data.blood_glucose_level, gen, chk]])
    model = artifacts["diabetes_xgb"]["model"]
    prob = float(model.predict_proba(features)[0][1])
    return {"risk_probability": prob, "risk_category": get_risk_category(prob)}

# CBC
@app.post("/analyze_cbc")
def analyze_cbc(input_data: CBCInput):
    # Simplified Logic
    findings = []
    if input_data.hemoglobin and input_data.hemoglobin < 12: findings.append("Low Hemoglobin")
    return {"summary": "Anemia suspected" if findings else "Normal", "findings": findings}

# Idiopathic
@app.post("/predict/idiopathic")
def predict_idiopathic(input_data: IdiopathicInput):
    if not artifacts["idiopathic"]["model"]: raise HTTPException(503, "Model not loaded")
    try:
        encs = artifacts["idiopathic"]["encoders"]
        scaler = artifacts["idiopathic"]["scaler"]
        # Robust input handling
        sex = encs['sex'].transform([input_data.gender.strip().lower()])[0]
        smoke = encs['smoking'].transform([input_data.smoking_history.strip().title()])[0]
        age = scaler.transform([[input_data.age]])[0][0]
        
        with torch.no_grad():
            prob = artifacts["idiopathic"]["model"](torch.FloatTensor([[age, sex, smoke]])).item()
        
        risk = 1.0 - prob # Assuming 0=IPF
        return {"prediction": "IPF" if risk > 0.5 else "Normal", "risk_probability": risk}
    except Exception as e: raise HTTPException(400, f"Error: {e}")

# NLP: ClinicalBERT
@app.post("/analyze/clinical_bert")
def analyze_text_bert(input_data: TextAnalysisInput):
    if not artifacts["nlp_bert"]: raise HTTPException(503, "ClinicalBERT not loaded")
    if "[MASK]" not in input_data.text: return {"error": "Text must contain [MASK] token"}
    return artifacts["nlp_bert"](input_data.text)

# NLP: Chat (Meditron)
@app.post("/chat/meditron")
def chat_meditron(input_data: ChatInput):
    try:
        response = ollama.chat(model="meditron-7b", messages=[{"role": "user", "content": input_data.message}])
        return {"response": response['message']['content']}
    except Exception as e:
        # Fallback if model not pulled or ollama not running
        raise HTTPException(503, f"Chat service unavailable: {e}. Ensure 'ollama serve' is running and 'meditron-7b' is pulled.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
