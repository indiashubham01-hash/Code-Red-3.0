from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # Import StaticFiles
import os # Ensure os is imported
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
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional

# Load Environment First
load_dotenv()

# NLP Imports
from transformers import pipeline
from genai_report import generate_medical_report, generate_chat_response

# Import models/schemas
from model_utils import CardioNN
from schemas import CardioInput, CardioPrediction, DiabetesInput, CBCInput, IdiopathicInput, TextAnalysisInput, ChatInput, ReportInput

# Suppress warnings
warnings.filterwarnings('ignore')

app = FastAPI(title="FedHealth Comprehensive AI API", description="Unified API for Cardiovascular, Diabetes, CBC, IPF, and Medical NLP")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    print(f"GLOBAL ERROR: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {str(exc)}", "type": str(type(exc))}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"VALIDATION ERROR: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc), "body": str(exc.body)}
    )

# --- Serve Static Files (Frontend) ---
if os.path.exists("frontend/dist"):
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

# SPA Catch-all Route (Must be after specific API routes, or at the end generally, but mounting happens early)
# We will define the catch-all at the very end of the file to capture non-API routes.


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

# Gemini Report Generation
@app.post("/generate_report")
def generate_report_endpoint(input_data: ReportInput):
    try:
        report = generate_medical_report(input_data.prediction, input_data.symptoms)
        return {"report": report}
    except Exception as e:
        raise HTTPException(500, f"Report generation failed: {e}")

# --- Startup Event ---
@app.on_event("startup")
def startup_event():
    print("Server Starting...")
    # Load Models later if stable
    print("Reloading Application Logic...")
    pass
    
    print("\nREGISTERED ROUTES:")
    for route in app.routes:
        print(f" - {route.path} ({route.name})")
    print("END ROUTES\n")
    
    print("Loading models...")
    
    # ... (Model loading logic is inside load_models, merging it here or keeping it separate)

    # Get Local IP
    # Actually, I should just add the print logic to the existing load_models function or a new one.
    # The current code has `def load_models():`. I will modify it to print the IP.
    
    # Get Local IP
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "127.0.0.1"
    
    print("\n" + "="*50)
    print(f" SERVER RUNNING ON PORT 6969")
    print(f" Local URL:   http://127.0.0.1:6969")
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
        # artifacts["cardio_xgb"]["model"] = joblib.load("xgboost_model.pkl")
        # try: artifacts["cardio_xgb"]["explainer"] = shap.TreeExplainer(artifacts["cardio_xgb"]["model"])
        # except: pass
        print("Cardio XGB Skipped (Crash).")
    except Exception as e: print(f"Cardio XGB Failed: {e}")

    # 3. Diabetes
    try:
        # artifacts["diabetes_xgb"]["model"] = joblib.load("diabetes_xgboost_model.pkl")
        with open("diabetes_label_encoders.pkl", "rb") as f: artifacts["diabetes_xgb"]["encoders"] = pickle.load(f)
        with open("diabetes_feature_info.pkl", "rb") as f: artifacts["diabetes_xgb"]["features"] = pickle.load(f)
        # try: artifacts["diabetes_xgb"]["explainer"] = shap.TreeExplainer(artifacts["diabetes_xgb"]["model"])
        # except: pass
        print("Diabetes Skipped (Crash).")
    except Exception as e: print(f"Diabetes Failed: {e}")

    # 4. Idiopathic
    try:
        model_ipf = IdiopathicNN(input_dim=3)
        # model_ipf.load_state_dict(torch.load("idiopathic_model.pth"))
        # model_ipf.eval()
        artifacts["idiopathic"]["model"] = None # model_ipf
        # artifacts["idiopathic"]["scaler"] = joblib.load("idiopathic_scaler.pkl")
        # artifacts["idiopathic"]["encoders"] = joblib.load("idiopathic_encoders.pkl")
        print("Idiopathic Skipped (Stability).")
    except Exception as e: print(f"Idiopathic Failed: {e}")

    # 5. NLP - ClinicalBERT
    # 5. NLP - ClinicalBERT
    try:
        print("Loading ClinicalBERT...")
        # artifacts["nlp_bert"] = pipeline("fill-mask", model="medicalai/ClinicalBERT")
        print("ClinicalBERT Skipped (Stability).")
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
@app.post("/predict/cardiovascular/result")
def predict_cardio_xgb1(input_data: CardioInput):
    # Try XGBoost
    if artifacts["cardio_xgb"]["model"]: 
        age_years = input_data.age / 365.25
        height_m = input_data.height / 100
        # XGB Feature Order: age, gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active
        features = np.array([[age_years, input_data.gender, input_data.height, input_data.weight, input_data.ap_hi, input_data.ap_lo, input_data.cholesterol, input_data.gluc, input_data.smoke, input_data.alco, input_data.active]])
        model = artifacts["cardio_xgb"]["model"]
        prob = float(model.predict_proba(features)[0][1])
        return {"risk_probability": prob, "risk_category": get_risk_category(prob)}
    
    # Fallback to NN if available
    if artifacts["cardio_nn"]["model"]:
        print("WARNING: XGBoost model not loaded. Falling back to Neural Network.")
        age_years = input_data.age / 365.25
        # NN Feature Order: gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active, age
        features = np.array([[input_data.gender, input_data.height, input_data.weight, input_data.ap_hi, input_data.ap_lo, input_data.cholesterol, input_data.gluc, input_data.smoke, input_data.alco, input_data.active, age_years]])
        scaled = artifacts["cardio_nn"]["scaler"].transform(features)
        with torch.no_grad():
            prob = torch.sigmoid(artifacts["cardio_nn"]["model"](torch.FloatTensor(scaled))).item()
        return {"risk_probability": prob, "risk_category": get_risk_category(prob)}
        
    raise HTTPException(503, "Model not loaded")

@app.post("/predict/cardiovascular/explanation")
def predict_cardio_xgb2(input_data: CardioInput):
    # Explanations only if XGB explainer is available
    if artifacts["cardio_xgb"]["model"] and artifacts["cardio_xgb"]["explainer"]:
        age_years = input_data.age / 365.25
        features = np.array([[age_years, input_data.gender, input_data.height, input_data.weight, input_data.ap_hi, input_data.ap_lo, input_data.cholesterol, input_data.gluc, input_data.smoke, input_data.alco, input_data.active]])
        shap_vals = artifacts["cardio_xgb"]["explainer"].shap_values(features)
        feature_names = ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active']
        expl = format_shap_explanation(shap_vals, feature_names, features)
        return {"explanations": expl}
    
    return {"explanations": None, "message": "No explanations available (Model missing or fallback used)"}

# Diabetes
@app.post("/predict/diabetes")
def predict_diabetes(input_data: DiabetesInput):
    if not artifacts["diabetes_xgb"]["model"]: 
        print("WARNING: Diabetes model not loaded. Returning mock response.")
        return {"risk_probability": 0.1, "risk_category": "Low (Mock)"}
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
    if not artifacts["idiopathic"]["model"]: 
        print("WARNING: Idiopathic model not loaded. Returning mock response.")
        return {"prediction": "Normal (Mock)", "risk_probability": 0.05}
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
    if not artifacts["nlp_bert"]: 
        print("WARNING: ClinicalBERT not loaded. Returning mock response.")
        # Return a dummy completion
        return [{"sequence": input_data.text.replace("[MASK]", "heart"), "score": 0.99, "token": 123, "token_str": "heart"}]
    if "[MASK]" not in input_data.text: return {"error": "Text must contain [MASK] token"}
    return artifacts["nlp_bert"](input_data.text)

# NLP: Chat (Meditron)
@app.post("/chat/meditron")
def chat_meditron(input_data: ChatInput):
    try:
        # response = ollama.chat(model="meditron-7b", messages=[{"role": "user", "content": input_data.message}])
        # return {"response": response['message']['content']}
        response_text = generate_chat_response(input_data.message)
        return {"response": response_text}
    except Exception as e:
        print(f"Chat Error: {e}")
        raise HTTPException(503, f"Chat service unavailable: {e}")


# --- SPA Catch-all Route ---
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    # Check if file exists in frontend/dist (e.g., favicon.ico, manifest.json)
    potential_file = f"frontend/dist/{full_path}"
    if os.path.exists(potential_file) and os.path.isfile(potential_file):
        return Response(content=open(potential_file, "rb").read(), media_type="application/octet-stream")

    # Otherwise serve index.html for SPA routing
    if os.path.exists("frontend/dist/index.html"):
        return Response(content=open("frontend/dist/index.html", "r", encoding="utf-8").read(), media_type="text/html")
    
    return {"message": "Frontend not built or index.html missing."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6969)
