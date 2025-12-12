# MedAssist Frontend Development Guide

This document provides specifications and design guidelines for building the React frontend for the MedAssist Comprehensive AI Backend.

## 1. System Overview
- **Backend URL**: `http://<HOST>:8004` (See console for IP)
- **Tech Stack**: React + Vite, Tailwind CSS, Framer Motion, Axios.
- **Goal**: A unified, aesthetic dashboard to access 5 distinct AI models.

## 2. Global Design Aesthetics
- **Theme**: Clean medical/scientific aesthetic.
- **Colors**:
    - Primary: Slate-900 / Indigo-600
    - Success (Low Risk): Emerald-500
    - Danger (High Risk): Rose-500
    - Background: Light gray/white with glassmorphism cards.
- **Typography**: Inter or Roboto (Clean sans-serif).
- **Interactions**: Smooth transitions between forms and results.

## 3. Feature Modules & Requirements

### A. Cardiovascular Disease
**Route**: `/predict/cardiovascular`
**UI Component**: `CardioForm.jsx`
**Inputs**:
| Field | Type | UI Element | Notes |
|-------|------|------------|-------|
| Age | Number | Input | Backend expects Years (convert if input is days) |
| Gender | Select | Dropdown | Male/Female |
| Height | Number | Input | cm |
| Weight | Number | Input | kg |
| Blood Pressure | Number x2 | Inputs | Systolic / Diastolic |
| Cholesterol | Select | Dropdown | Normal/Above Normal/Well Above |
| Glucose | Select | Dropdown | Normal/Above Normal/Well Above |
| Lifestyle | Checkbox | Toggles | Smoke, Alcohol, Active |

**Result Display**:
- **Risk Category**: "High/Medium/Low" (Color coded)
- **Probability**: Progress bar or Gauge chart.
- **SHAP Explanation**: Bar chart showing top factors increasing risk.

---

### B. Diabetes Prediction
**Route**: `/predict/diabetes`
**UI Component**: `DiabetesForm.jsx`
**Inputs**:
- Age, BMI, HbA1c, Blood Glucose.
- Hypertension, Heart Disease (Toggles).
- Smoking History (Dropdown: Ever, Never, Former, Current, No Info).

**Result Display**:
- Simple Risk Score (0-100%).
- Recommendation lists based on risk.

---

### C. Idiopathic Pulmonary Fibrosis (IPF)
**Route**: `/predict/idiopathic`
**UI Component**: `IPFForm.jsx`
**Inputs**:
- Age (Years).
- Gender (Male/Female).
- Smoking History (Ever/Never).

**Result Display**:
- **Prediction**: "IPF Suspected" vs "Normal".
- **Risk Probability**: Pie chart.

---

### D. CBC Analysis
**Route**: `/analyze_cbc`
**UI Component**: `CBCUpload.jsx` or Form
**Inputs**:
- WBC, RBC, Hemoglobin, Hematocrit, Platelets, MCV, MCH, MCHC, RDW.
- Sex (Male/Female) - *Critical for range calculation*.

**Result Display**:
- **Summary**: Text paragraph describing abnormalities.
- **Detailed Table**: List of parameters with "Normal/Low/High" flags (use Icons).

---

### E. Medical AI Chat & Analysis
**Routes**: `/chat/meditron`, `/analyze/clinical_bert`
**UI Component**: `MedicalAssistant.jsx`

#### 1. Clinical Text Analysis
- **Input**: Text Area for medical notes.
- **Feature**: User types "Patient has [MASK] pain." -> AI fills the blank.
- **Display**: Chip/Badge list of predicted words with confidence scores.

#### 2. AI Chatbot
- **Input**: Chat interface (Message bubble style).
- **State**: Maintain history list in React state (though backend is stateless for now).
- **UI**: Typical chat window (User right, AI left).

## 4. API Integration Pattern (React)

```javascript
// Example Service Hook
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8004';

export const predictCardio = async (data) => {
  try {
    const res = await axios.post(`${API_URL}/predict/cardiovascular`, data);
    return res.data;
  } catch (err) {
    console.error(err);
    throw err;
  }
};
```

## 5. Error Handling
- **404/503**: Show "Service Unavailable" banner.
- **400 (Validation)**: Highlight invalid form fields (e.g., "Age must be positive").
- **Loading State**: Disable submit button and show spinner during all API calls.
