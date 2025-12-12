"""
MedAssist Prediction API
Flask API for Cardiovascular and Diabetes Risk Prediction with SHAP Explanations

This API provides endpoints for:
1. Cardiovascular disease prediction
2. Diabetes risk prediction

Both endpoints return predictions, confidence scores, and SHAP explanations.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pickle
import numpy as np
import pandas as pd
import shap
import warnings
from typing import Dict, List, Tuple, Any
import logging
import os

# Suppress warnings
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables to store models and explainers
cardio_model = None
diabetes_model = None
diabetes_encoders = None
diabetes_features = None
cardio_explainer = None
diabetes_explainer = None

def load_models():
    """Load all models and create SHAP explainers"""
    global cardio_model, diabetes_model, diabetes_encoders, diabetes_features
    global cardio_explainer, diabetes_explainer
    
    try:
        # Load cardiovascular model
        cardio_model = joblib.load('xgboost_model.pkl')
        logger.info("Cardiovascular model loaded successfully")
        
        # Load diabetes model and encoders
        diabetes_model = joblib.load('diabetes_xgboost_model.pkl')
        
        with open('diabetes_label_encoders.pkl', 'rb') as f:
            diabetes_encoders = pickle.load(f)
            
        with open('diabetes_feature_info.pkl', 'rb') as f:
            diabetes_features = pickle.load(f)
            
        logger.info("Diabetes model and encoders loaded successfully")
        
        # Create SHAP explainers
        cardio_explainer = shap.TreeExplainer(cardio_model)
        diabetes_explainer = shap.TreeExplainer(diabetes_model)
        logger.info("SHAP explainers created successfully")
        
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        raise e

def get_risk_category(probability: float) -> str:
    """Categorize risk based on probability"""
    if probability < 0.3:
        return 'Low'
    elif probability < 0.7:
        return 'Medium'
    else:
        return 'High'

def format_shap_explanation(shap_values: np.ndarray, feature_names: List[str], 
                          feature_values: np.ndarray) -> Dict[str, Any]:
    """Format SHAP values into interpretable explanations"""
    explanations = []
    
    # Get the SHAP values for the first sample
    # For XGBoost binary classification, shap_values is 2D: (samples, features)
    if len(shap_values.shape) == 2:
        shap_vals = shap_values[0]  # Get SHAP values for the first sample
    else:
        # Handle other cases (e.g., 1D array)
        shap_vals = shap_values
    
    for i, (feature, shap_val, feature_val) in enumerate(zip(feature_names, shap_vals, feature_values[0])):
        impact = "increases" if shap_val > 0 else "decreases"
        explanations.append({
            'feature': feature,
            'value': float(feature_val),
            'shap_value': float(shap_val),
            'impact': impact,
            'importance': abs(float(shap_val))
        })
    
    # Sort by importance (absolute SHAP value)
    explanations.sort(key=lambda x: x['importance'], reverse=True)
    
    return {
        'explanations': explanations,
        'top_factors': explanations[:5],  # Top 5 most important factors
        'summary': generate_explanation_summary(explanations[:3])
    }

def generate_explanation_summary(top_explanations: List[Dict]) -> str:
    """Generate human-readable explanation summary"""
    if not top_explanations:
        return "Unable to generate explanation summary."
    
    summary_parts = []
    for exp in top_explanations:
        feature = exp['feature'].replace('_', ' ').title()
        impact = exp['impact']
        value = exp['value']
        
        summary_parts.append(f"{feature} (value: {value:.2f}) {impact} the risk")
    
    return f"The prediction is primarily influenced by: {', '.join(summary_parts)}."

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'MedAssist Prediction API is running',
        'models_loaded': {
            'cardiovascular': cardio_model is not None,
            'diabetes': diabetes_model is not None
        }
    })

@app.route('/predict/cardiovascular', methods=['POST'])
def predict_cardiovascular():
    """
    Predict cardiovascular disease risk
    
    Expected JSON input:
    {
        "age": float (in days, will be converted to years),
        "gender": int (1=female, 2=male),
        "height": float (in cm),
        "weight": float (in kg),
        "ap_hi": int (systolic blood pressure),
        "ap_lo": int (diastolic blood pressure),
        "cholesterol": int (1=normal, 2=above normal, 3=well above normal),
        "gluc": int (1=normal, 2=above normal, 3=well above normal),
        "smoke": int (0=no, 1=yes),
        "alco": int (0=no, 1=yes),
        "active": int (0=no, 1=yes)
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 
                          'cholesterol', 'gluc', 'smoke', 'alco', 'active']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}'
            }), 400
        
        # Convert age from days to years if needed (assuming input is in days as per original dataset)
        age_years = data['age'] / 365.25 if data['age'] > 150 else data['age']
        
        # Calculate BMI
        height_m = data['height'] / 100  # Convert cm to meters
        bmi = data['weight'] / (height_m ** 2)
        
        # Prepare features for prediction
        # Note: The exact feature order should match the training data
        features = np.array([[
            age_years,
            data['gender'],
            data['height'],
            data['weight'],
            data['ap_hi'],
            data['ap_lo'],
            data['cholesterol'],
            data['gluc'],
            data['smoke'],
            data['alco'],
            data['active']
        ]])
        
        feature_names = ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 
                        'cholesterol', 'gluc', 'smoke', 'alco', 'active']
        
        # Make prediction
        prediction = cardio_model.predict(features)[0]
        prediction_proba = cardio_model.predict_proba(features)[0]
        confidence = float(max(prediction_proba))
        risk_probability = float(prediction_proba[1])  # Probability of having cardiovascular disease
        
        # Generate SHAP explanations
        shap_values = cardio_explainer.shap_values(features)
        explanations = format_shap_explanation(shap_values, feature_names, features)
        
        # Determine risk category
        risk_category = get_risk_category(risk_probability)
        
        result = {
            'prediction': int(prediction),
            'risk_probability': risk_probability,
            'confidence_score': confidence,
            'risk_category': risk_category,
            'input_data': {
                'age_years': round(age_years, 1),
                'bmi': round(bmi, 2),
                'gender': 'Female' if data['gender'] == 1 else 'Male',
                'systolic_bp': data['ap_hi'],
                'diastolic_bp': data['ap_lo'],
                'cholesterol_level': data['cholesterol'],
                'glucose_level': data['gluc'],
                'smoking': bool(data['smoke']),
                'alcohol': bool(data['alco']),
                'physical_activity': bool(data['active'])
            },
            'explanations': explanations,
            'interpretation': {
                'result': 'High risk of cardiovascular disease' if prediction == 1 else 'Low risk of cardiovascular disease',
                'recommendation': get_cardio_recommendations(risk_category, explanations['top_factors'])
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in cardiovascular prediction: {str(e)}")
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/predict/diabetes', methods=['POST'])
def predict_diabetes():
    """
    Predict diabetes risk
    
    Expected JSON input:
    {
        "age": float,
        "gender": str ("Female", "Male", "Other"),
        "hypertension": int (0 or 1),
        "heart_disease": int (0 or 1),
        "smoking_history": str ("never", "No Info", "current", "former", "ever", "not current"),
        "bmi": float,
        "HbA1c_level": float,
        "blood_glucose_level": int
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['age', 'gender', 'hypertension', 'heart_disease', 
                          'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}'
            }), 400
        
        # Validate categorical values
        valid_genders = ['Female', 'Male', 'Other']
        valid_smoking = ['never', 'No Info', 'current', 'former', 'ever', 'not current']
        
        if data['gender'] not in valid_genders:
            return jsonify({
                'error': f'Invalid gender. Must be one of: {valid_genders}'
            }), 400
            
        if data['smoking_history'] not in valid_smoking:
            return jsonify({
                'error': f'Invalid smoking_history. Must be one of: {valid_smoking}'
            }), 400
        
        # Encode categorical variables
        try:
            gender_encoded = diabetes_encoders['gender_encoder'].transform([data['gender']])[0]
            smoking_encoded = diabetes_encoders['smoking_encoder'].transform([data['smoking_history']])[0]
        except ValueError as e:
            return jsonify({
                'error': f'Invalid categorical value: {str(e)}'
            }), 400
        
        # Prepare features for prediction
        features = np.array([[
            data['age'],
            data['hypertension'], 
            data['heart_disease'],
            data['bmi'],
            data['HbA1c_level'],
            data['blood_glucose_level'],
            gender_encoded,
            smoking_encoded
        ]])
        
        feature_names = diabetes_features['feature_names']
        
        # Make prediction
        prediction = diabetes_model.predict(features)[0]
        prediction_proba = diabetes_model.predict_proba(features)[0]
        confidence = float(max(prediction_proba))
        risk_probability = float(prediction_proba[1])  # Probability of having diabetes
        
        # Generate SHAP explanations
        shap_values = diabetes_explainer.shap_values(features)
        explanations = format_shap_explanation(shap_values, feature_names, features)
        
        # Determine risk category
        risk_category = get_risk_category(risk_probability)
        
        result = {
            'prediction': int(prediction),
            'risk_probability': risk_probability,
            'confidence_score': confidence,
            'risk_category': risk_category,
            'input_data': {
                'age': data['age'],
                'gender': data['gender'],
                'bmi': data['bmi'],
                'bmi_category': get_bmi_category(data['bmi']),
                'hypertension': bool(data['hypertension']),
                'heart_disease': bool(data['heart_disease']),
                'smoking_history': data['smoking_history'],
                'HbA1c_level': data['HbA1c_level'],
                'HbA1c_category': get_hba1c_category(data['HbA1c_level']),
                'blood_glucose_level': data['blood_glucose_level'],
                'glucose_category': get_glucose_category(data['blood_glucose_level'])
            },
            'explanations': explanations,
            'interpretation': {
                'result': 'High risk of diabetes' if prediction == 1 else 'Low risk of diabetes',
                'recommendation': get_diabetes_recommendations(risk_category, explanations['top_factors'])
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in diabetes prediction: {str(e)}")
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

def get_bmi_category(bmi: float) -> str:
    """Categorize BMI"""
    if bmi < 18.5:
        return 'Underweight'
    elif bmi < 25:
        return 'Normal weight'
    elif bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'

def get_hba1c_category(hba1c: float) -> str:
    """Categorize HbA1c levels"""
    if hba1c < 5.7:
        return 'Normal'
    elif hba1c < 6.5:
        return 'Prediabetes'
    else:
        return 'Diabetes'

def get_glucose_category(glucose: int) -> str:
    """Categorize blood glucose levels"""
    if glucose < 100:
        return 'Normal'
    elif glucose < 126:
        return 'Prediabetes'
    else:
        return 'Diabetes'

def get_cardio_recommendations(risk_category: str, top_factors: List[Dict]) -> List[str]:
    """Generate cardiovascular health recommendations"""
    recommendations = []
    
    if risk_category == 'High':
        recommendations.append("Consult with a cardiologist immediately for comprehensive evaluation")
        recommendations.append("Consider immediate lifestyle modifications including diet and exercise")
    elif risk_category == 'Medium':
        recommendations.append("Schedule regular check-ups with your healthcare provider")
        recommendations.append("Implement preventive lifestyle changes")
    else:
        recommendations.append("Maintain current healthy lifestyle")
        recommendations.append("Continue regular health screenings")
    
    # Add specific recommendations based on top risk factors
    for factor in top_factors[:3]:
        feature = factor['feature']
        if feature == 'ap_hi' and factor['impact'] == 'increases':
            recommendations.append("Monitor and manage blood pressure through diet, exercise, and medication if needed")
        elif feature == 'cholesterol' and factor['impact'] == 'increases':
            recommendations.append("Consider cholesterol management through diet and possible medication")
        elif feature == 'smoke' and factor['impact'] == 'increases':
            recommendations.append("Smoking cessation is highly recommended")
        elif feature == 'active' and factor['impact'] == 'decreases':
            recommendations.append("Increase physical activity and exercise regularly")
    
    return recommendations

def get_diabetes_recommendations(risk_category: str, top_factors: List[Dict]) -> List[str]:
    """Generate diabetes prevention/management recommendations"""
    recommendations = []
    
    if risk_category == 'High':
        recommendations.append("Consult with an endocrinologist or diabetes specialist immediately")
        recommendations.append("Consider comprehensive diabetes screening and monitoring")
    elif risk_category == 'Medium':
        recommendations.append("Schedule regular glucose monitoring and healthcare check-ups")
        recommendations.append("Implement diabetes prevention strategies")
    else:
        recommendations.append("Maintain current healthy lifestyle")
        recommendations.append("Continue regular health screenings")
    
    # Add specific recommendations based on top risk factors
    for factor in top_factors[:3]:
        feature = factor['feature']
        if feature == 'HbA1c_level' and factor['impact'] == 'increases':
            recommendations.append("Focus on blood sugar control through diet and lifestyle modifications")
        elif feature == 'blood_glucose_level' and factor['impact'] == 'increases':
            recommendations.append("Monitor blood glucose levels regularly and maintain healthy diet")
        elif feature == 'bmi' and factor['impact'] == 'increases':
            recommendations.append("Weight management through balanced diet and regular exercise")
        elif feature == 'age' and factor['impact'] == 'increases':
            recommendations.append("Regular health screenings become more important with age")
    
    return recommendations

@app.route('/model/info', methods=['GET'])
def model_info():
    """Get information about the loaded models"""
    cardio_info = {
        'loaded': cardio_model is not None,
        'type': 'XGBoost Classifier',
        'purpose': 'Cardiovascular Disease Prediction',
        'features': ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 
                    'cholesterol', 'gluc', 'smoke', 'alco', 'active']
    }
    
    diabetes_info = {
        'loaded': diabetes_model is not None,
        'type': 'XGBoost Classifier', 
        'purpose': 'Diabetes Risk Prediction',
        'features': diabetes_features['feature_names'] if diabetes_features else []
    }
    
    return jsonify({
        'cardiovascular_model': cardio_info,
        'diabetes_model': diabetes_info,
        'shap_explanations': 'Available for both models'
    })


NORMAL_RANGES = {
    'male': {
        'rbc': (4.5, 5.9),        # Red Blood Cell Count (x10^12/L)
        'hemoglobin': (13.5, 17.5), # (g/dL)
        'hematocrit': (41, 53),     # (%)
    },
    'female': {
        'rbc': (4.0, 5.2),
        'hemoglobin': (12.0, 15.5),
        'hematocrit': (36, 46),
    },
    'common': {
        # These parameters have ranges that are generally not sex-dependent
        'wbc': (4.5, 11.0),       # White Blood Cell Count (x10^9/L)
        'platelets': (150, 450),  # (x10^9/L)
        'mcv': (80, 100),         # Mean Corpuscular Volume (fL)
        'mch': (27, 32),          # Mean Corpuscular Hemoglobin (pg)
        'mchc': (32, 36),         # Mean Corpuscular Hemoglobin Concentration (g/dL)
        'rdw': (11.5, 14.5)       # Red Cell Distribution Width (%)
    }
}

UNITS = {
    'wbc': 'x10^9/L',
    'rbc': 'x10^12/L',
    'hemoglobin': 'g/dL',
    'hematocrit': '%',
    'platelets': 'x10^9/L',
    'mcv': 'fL',
    'mch': 'pg',
    'mchc': 'g/dL',
    'rdw': '%'
}

# --- Core Analysis Logic ---

def analyze_cbc(sex: str, cbc_data: dict) -> dict:
    """
    Analyzes provided CBC data against predefined normal ranges based on sex.

    Args:
        sex (str): The patient's sex ('male' or 'female').
        cbc_data (dict): A dictionary of CBC parameters and their values.

    Returns:
        dict: A dictionary containing a summary and a detailed analysis.
    """
    findings = []
    abnormalities = []

    # Combine common ranges with the appropriate sex-specific ranges
    applicable_ranges = {**NORMAL_RANGES['common'], **NORMAL_RANGES[sex]}

    for param, value in cbc_data.items():
        param_lower = param.lower()
        if param_lower in applicable_ranges:
            low_bound, high_bound = applicable_ranges[param_lower]
            unit = UNITS.get(param_lower, '')
            status = "Normal"

            # Check if the value is outside the normal range
            if value < low_bound:
                status = "Low"
                abnormalities.append(f"{param.upper()} is low")
            elif value > high_bound:
                status = "High"
                abnormalities.append(f"{param.upper()} is high")

            findings.append({
                "parameter": param.upper(),
                "value": value,
                "status": status,
                "normal_range": f"{low_bound} - {high_bound} {unit}"
            })

    # Generate a concise summary of the findings
    if not abnormalities:
        summary = "All provided CBC parameters are within the normal range."
    else:
        summary = ". ".join(abnormalities) + "."

    return {"summary": summary, "detailed_analysis": findings}


# --- API Endpoint Definition ---

@app.route('/analyze_cbc', methods=['POST'])
def cbc_analyzer_api():
    """
    API endpoint to receive and process a CBC analysis request.
    """
    # 1. Get and validate the JSON payload from the request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    # 2. Validate mandatory 'sex' parameter
    sex = data.get('sex', '').lower()
    if sex not in ['male', 'female']:
        return jsonify({
            "error": "Mandatory parameter 'sex' is missing or invalid. Must be 'male' or 'female'."
        }), 400

    # 3. Extract CBC parameters, excluding 'sex'
    cbc_params = {k.lower(): v for k, v in data.items() if k.lower() != 'sex'}

    if not cbc_params:
        return jsonify({"error": "No CBC parameters provided for analysis."}), 400

    # 4. Ensure all provided CBC values are numeric
    try:
        cbc_params_numeric = {k: float(v) for k, v in cbc_params.items()}
    except (ValueError, TypeError):
        return jsonify({"error": "All CBC parameter values must be numeric."}), 400

    # 5. Call the analysis function and return the result
    result = analyze_cbc(sex, cbc_params_numeric)
    return jsonify(result), 200



if __name__ == '__main__':
    # Load models on startup
    try:
        load_models()
        logger.info("All models loaded successfully. Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=5001)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        print(f"Error: {str(e)}")
