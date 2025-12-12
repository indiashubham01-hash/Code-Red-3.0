# Cardio Disease Prediction API Documentation

This document outlines the specifications for the backend API, intended to guide the frontend development.

## Overview
The API provides a machine learning interface to predict the presence of cardiovascular disease based on user health metrics.

**Base URL**: `http://<HOST>:8001`
- **Local**: `http://127.0.0.1:8001`
- **Network**: `http://<YOUR_LOCAL_IP>:8001` (The exact URL is logged to the console at startup)

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

### 2. Cardiovascular Disease Prediction (XGBoost + SHAP)
*New endpoint with detailed explanations.*
- **URL**: `/predict/cardiovascular`
- **Method**: `POST`
- **Input**: same as `/predict`
- **Output**: Detailed JSON with `risk_category`, `explanations`, `recommendations`.

### 3. Diabetes Risk Prediction
- **URL**: `/predict/diabetes`
- **Method**: `POST`
- **Input**:
  ```json
  {
    "age": 45,
    "gender": "Male",
    "hypertension": 1,
    "heart_disease": 0,
    "smoking_history": "former",
    "bmi": 28.5,
    "HbA1c_level": 6.2,
    "blood_glucose_level": 140
  }
  ```

### 4. CBC Analysis
- **URL**: `/analyze_cbc`
- **Method**: `POST`
- **Input**:
  ```json
  {
    "sex": "male",
    "wbc": 8.5,
    "rbc": 4.8,
    "hemoglobin": 14.2,
    "hematocrit": 42,
    "platelets": 280
    // ... other parameters
  }
  ```

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

axios.post('http://127.0.0.1:8001/predict/diabetes', diabetesData)
  .then(response => console.log(response.data));
```
