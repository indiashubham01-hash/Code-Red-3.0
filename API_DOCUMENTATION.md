# Cardio Disease Prediction API Documentation

This document outlines the specifications for the backend API, intended to guide the frontend development.

## Overview
The API provides a machine learning interface to predict the presence of cardiovascular disease based on user health metrics.

**Base URL**: `http://<HOST>:6969`
- **Local**: `http://127.0.0.1:6969`
- **Network**: `http://<YOUR_LOCAL_IP>:6969` (The exact URL is logged to the console at startup)

---

## Endpoints

### 1. Health Check & Documentation
- **GET /**: Root endpoint (returns 404 by default, meant for verification).
- **GET /docs**: Interactive Swagger UI documentation.
- **GET /redoc**: ReDoc documentation.

### 2. Predict Disease Risk
**Route**: `POST /predict`

**Description**: Accepts health parameters and returns the probability of cardiovascular disease.

#### Request Specification
**Content-Type**: `application/json`

**Body Fields**:

| Field | Type | Description | Accepted Values / Range |
### 1. Cardiovascular Disease Prediction (Neural Network)
*Original endpoint used by the React App.*
- **URL**: `/predict`
- **Method**: `POST`
- **Input**: `CardioInput`
- **Output**: `CardioPrediction`

### 2. Cardiovascular Disease (XGBoost)
- **Result Endpoint**: `POST /predict/cardiovascular/result`
    - Returns: `{"risk_probability": float, "risk_category": string}`
    - Fallback: Automatically uses Neural Network if XGBoost fails.
- **Explanation Endpoint**: `POST /predict/cardiovascular/explanation`
    - Returns: `{"explanations": {...}}` or `{"explanations": null}`
    - Use: Optional second call for detailed SHAP analysis.

### 3. Diabetes Risk Prediction
- **URL**: `/predict/diabetes`
- **Method**: `POST`
- **Input**:
  ```json
  {
    "age": 45,                  // Age in years (float)
    "gender": "Male",           // "Male", "Female", "Other"
    "hypertension": 1,          // 0: No, 1: Yes
    "heart_disease": 0,         // 0: No, 1: Yes
    "smoking_history": "former",// "never", "No Info", "current", "former", "ever", "not current"
    "bmi": 28.5,                // Body Mass Index
    "HbA1c_level": 6.2,         // Hemoglobin A1c (3.5 - 9.0)
    "blood_glucose_level": 140  // Blood Glucose (80 - 300)
  }
  ```

### 4. CBC Analysis (Blood Count)
- **URL**: `/analyze_cbc`
- **Method**: `POST`
- **Input**:
  ```json
  {
    "sex": "male",              // "male" or "female" (for reference ranges)
    "wbc": 8.5,                 // White Blood Cells (x10^9/L)
    "rbc": 4.8,                 // Red Blood Cells (x10^12/L)
    "hemoglobin": 14.2,         // Hemoglobin (g/dL)
    "hematocrit": 42,           // Hematocrit (%)
    "platelets": 280,           // Platelets (x10^9/L)
    "mcv": 88,                  // Mean Corpuscular Volume (fL)
    "mch": 30,                  // Mean Corpuscular Hemoglobin (pg)
    "mchc": 34,                 // Mean Corpuscular Hemoglobin Concentration (g/dL)
    "rdw": 12.5                 // Red Cell Distribution Width (%)
  }
  ```
- **Output**: Analysis summary and specific findings (e.g., "Anemia Suspected").

### 5. Health Check
- **URL**: `/health`
- **Method**: `GET`
- **Response**: Status of all loaded models.

---

## Usage Examples

### React/JS
```javascript
// Diabetes Prediction
const diabetesData = {
  age: 45,
  gender: "Male",
  hypertension: 1,
  heart_disease: 0,
  smoking_history: "former",
  bmi: 28.5,
  HbA1c_level: 6.2,
  blood_glucose_level: 140
};

axios.post('http://127.0.0.1:6969/predict/diabetes', diabetesData)
  .then(response => console.log(response.data));
```
