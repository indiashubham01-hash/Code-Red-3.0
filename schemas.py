from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union, Any

class CardioInput(BaseModel):
    age: int = Field(..., description="Age in days")
    gender: int = Field(..., description="Gender analysis (1: women, 2: men)")
    height: int = Field(..., description="Height in cm")
    weight: float = Field(..., description="Weight in kg")
    ap_hi: int = Field(..., description="Systolic blood pressure")
    ap_lo: int = Field(..., description="Diastolic blood pressure")
    cholesterol: int = Field(..., description="Cholesterol (1: normal, 2: above normal, 3: well above normal)")
    gluc: int = Field(..., description="Glucose (1: normal, 2: above normal, 3: well above normal)")
    smoke: int = Field(..., description="Smoking (0: no, 1: yes)")
    alco: int = Field(..., description="Alcohol intake (0: no, 1: yes)")
    active: int = Field(..., description="Physical activity (0: no, 1: yes)")

    class Config:
        json_schema_extra = {
            "example": {
                "age": 18393,
                "gender": 2,
                "height": 168,
                "weight": 62.0,
                "ap_hi": 110,
                "ap_lo": 80,
                "cholesterol": 1,
                "gluc": 1,
                "smoke": 0,
                "alco": 0,
                "active": 1
            }
        }

class CardioPrediction(BaseModel):
    probability: float
    prediction: int
    message: str

# --- New Models ---

class DiabetesInput(BaseModel):
    age: float = Field(..., description="Age in years")
    gender: str = Field(..., description="Gender: 'Female', 'Male', 'Other'")
    hypertension: int = Field(..., description="0: No, 1: Yes")
    heart_disease: int = Field(..., description="0: No, 1: Yes")
    smoking_history: str = Field(..., description="'never', 'No Info', 'current', 'former', 'ever', 'not current'")
    bmi: float = Field(..., description="Body Mass Index")
    HbA1c_level: float = Field(..., description="Hemoglobin A1c level (3.5-9.0)")
    blood_glucose_level: int = Field(..., description="Blood glucose level (80-300)")

    class Config:
        json_schema_extra = {
            "example": {
                "age": 45,
                "gender": "Male",
                "hypertension": 1,
                "heart_disease": 0,
                "smoking_history": "former",
                "bmi": 28.5,
                "HbA1c_level": 6.2,
                "blood_glucose_level": 140
            }
        }

class CBCInput(BaseModel):
    sex: str = Field(..., description="'male' or 'female'")
    wbc: Optional[float] = Field(None, description="White Blood Cell Count (x10^9/L)")
    rbc: Optional[float] = Field(None, description="Red Blood Cell Count (x10^12/L)")
    hemoglobin: Optional[float] = Field(None, description="Hemoglobin level (g/dL)")
    hematocrit: Optional[float] = Field(None, description="Hematocrit percentage (%)")
    platelets: Optional[float] = Field(None, description="Platelet Count (x10^9/L)")
    mcv: Optional[float] = Field(None, description="Mean Corpuscular Volume (fL)")
    mch: Optional[float] = Field(None, description="Mean Corpuscular Hemoglobin (pg)")
    mchc: Optional[float] = Field(None, description="Mean Corpuscular Hemoglobin Concentration (g/dL)")
    rdw: Optional[float] = Field(None, description="Red Cell Distribution Width (%)")

    class Config:
        json_schema_extra = {
            "example": {
                "sex": "male",
                "wbc": 8.5,
                "rbc": 4.8,
                "hemoglobin": 14.2,
                "hematocrit": 42,
                "platelets": 280
            }
        }

class IdiopathicInput(BaseModel):
    age: int = Field(..., description="Age in years")
    gender: str = Field(..., description="'Male' or 'Female'")
    smoking_history: str = Field(..., description="'Ever' or 'Never'")

    class Config:
        json_schema_extra = {
            "example": {
                "age": 65,
                "gender": "Male",
                "smoking_history": "Ever"
            }
        }

class TextAnalysisInput(BaseModel):
    text: str = Field(..., description="Medical text to analyze (e.g., masked sentence)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "The patient was prescribed [MASK] for hypertension."
            }
        }

class ChatInput(BaseModel):
    message: str = Field(..., description="Question for the medical AI")
    history: Optional[List[Dict[str, str]]] = Field(default=[], description="Chat history")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "What are the symptoms of Type 2 Diabetes?",
                "history": []
            }
        }

class ReportInput(BaseModel):
    prediction: Dict[str, Any] = Field(..., description="Prediction result from other endpoints")
    symptoms: List[str] = Field(default=[], description="List of patient symptoms")

    class Config:
        json_schema_extra = {
            "example": {
                "prediction": {"risk_probability": 0.85, "risk_category": "High"},
                "symptoms": ["Chest pain", "Shortness of breath"]
            }
        }



class StandardPredictionResponse(BaseModel):
    # Unified response format for consistency if needed, but for now we follow the Flask API format loosely or stricter
    prediction: int
    risk_probability: float
    confidence_score: float
    risk_category: str
    input_data: Dict[str, Any]
    feature_importance: Optional[List[Dict[str, Any]]] = None
    interpretation: Dict[str, Any]
