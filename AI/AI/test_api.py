"""
MedAssist API Test Suite
Test file to demonstrate all three API endpoints with sample data

This file tests:
1. Cardiovascular Disease Prediction API
2. Diabetes Risk Prediction API  
3. CBC (Complete Blood Count) Analysis API

Each test shows the input data and then calls the respective API to display results.
"""

import requests
import json
import time
from typing import Dict, Any

# API Base URL
BASE_URL = "http://localhost:5001"

def print_separator(title: str):
    """Print a nice separator with title"""
    print("\n" + "="*80)
    print(f" {title} ".center(80, "="))
    print("="*80)

def print_data_display(title: str, data: Dict[Any, Any]):
    """Display data in a formatted way"""
    print(f"\n📊 {title}:")
    print("-" * 60)
    for key, value in data.items():
        print(f"  {key}: {value}")

def make_api_request(endpoint: str, data: Dict[Any, Any]) -> Dict[Any, Any]:
    """Make API request and handle response"""
    try:
        print(f"\n🔄 Making API request to: {endpoint}")
        response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=30)
        
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error Response: {response.text}")
            return {"error": f"HTTP {response.status_code}: {response.text}"}
            
    except requests.exceptions.ConnectionError:
        return {"error": "Connection failed. Make sure the API server is running on port 5001"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def display_prediction_results(result: Dict[Any, Any], prediction_type: str):
    """Display prediction results in a formatted way"""
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return
    
    print(f"\n🎯 {prediction_type} Prediction Results:")
    print("-" * 60)
    
    # Main prediction info
    prediction = result.get('prediction', 'Unknown')
    risk_prob = result.get('risk_probability', 0)
    confidence = result.get('confidence_score', 0)
    risk_category = result.get('risk_category', 'Unknown')
    
    print(f"  🔮 Prediction: {'High Risk' if prediction == 1 else 'Low Risk'}")
    print(f"  📊 Risk Probability: {risk_prob:.3f} ({risk_prob*100:.1f}%)")
    print(f"  🎯 Confidence Score: {confidence:.3f} ({confidence*100:.1f}%)")
    print(f"  ⚠️  Risk Category: {risk_category}")
    
    # Interpretation
    interpretation = result.get('interpretation', {})
    if interpretation:
        print(f"\n💡 Interpretation:")
        print(f"  📝 Result: {interpretation.get('result', 'N/A')}")
        
        recommendations = interpretation.get('recommendation', [])
        if recommendations:
            print(f"  💊 Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"    {i}. {rec}")
    
    # Top factors from SHAP analysis
    explanations = result.get('explanations', {})
    top_factors = explanations.get('top_factors', [])
    if top_factors:
        print(f"\n🔍 Top Risk Factors (SHAP Analysis):")
        for i, factor in enumerate(top_factors[:5], 1):
            feature = factor['feature'].replace('_', ' ').title()
            impact = factor['impact']
            importance = factor['importance']
            value = factor['value']
            print(f"    {i}. {feature}: {value:.2f} ({impact} risk, importance: {importance:.3f})")
    
    # Summary explanation
    summary = explanations.get('summary', '')
    if summary:
        print(f"\n📋 Summary: {summary}")

def display_cbc_results(result: Dict[Any, Any]):
    """Display CBC analysis results"""
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return
    
    print(f"\n🩸 CBC Analysis Results:")
    print("-" * 60)
    
    summary = result.get('summary', 'No summary available')
    print(f"📋 Summary: {summary}")
    
    detailed_analysis = result.get('detailed_analysis', [])
    if detailed_analysis:
        print(f"\n📊 Detailed Analysis:")
        print(f"{'Parameter':<15} {'Value':<10} {'Status':<10} {'Normal Range':<20}")
        print("-" * 65)
        
        for item in detailed_analysis:
            param = item.get('parameter', 'N/A')
            value = item.get('value', 'N/A')
            status = item.get('status', 'N/A')
            normal_range = item.get('normal_range', 'N/A')
            
            # Add color-like indicators
            status_indicator = "✅" if status == "Normal" else "⚠️" if status == "Low" else "🔴"
            
            print(f"{param:<15} {value:<10} {status_indicator}{status:<9} {normal_range:<20}")

def test_health_endpoint():
    """Test the health check endpoint"""
    print_separator("HEALTH CHECK")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"📡 Health Check Response: {response.status_code}")
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ API Status: {health_data.get('status', 'Unknown')}")
            print(f"📝 Message: {health_data.get('message', 'No message')}")
            
            models_loaded = health_data.get('models_loaded', {})
            print(f"🤖 Models Loaded:")
            for model_type, loaded in models_loaded.items():
                status = "✅ Loaded" if loaded else "❌ Not Loaded"
                print(f"    {model_type.title()}: {status}")
            
            return True
        else:
            print(f"❌ Health check failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_cardiovascular_prediction():
    """Test cardiovascular disease prediction with sample data"""
    print_separator("CARDIOVASCULAR DISEASE PREDICTION TEST")
    
    # Sample data for cardiovascular prediction
    cardio_test_data = {
        "age": 50 * 365.25,  # Age in days (50 years)
        "gender": 2,         # Male (1=female, 2=male)
        "height": 175,       # Height in cm
        "weight": 80,        # Weight in kg
        "ap_hi": 140,        # Systolic blood pressure (high)
        "ap_lo": 90,         # Diastolic blood pressure (high)
        "cholesterol": 3,    # Well above normal (1=normal, 2=above normal, 3=well above normal)
        "gluc": 2,           # Above normal glucose (1=normal, 2=above normal, 3=well above normal)
        "smoke": 1,          # Smoker (0=no, 1=yes)
        "alco": 0,           # No alcohol (0=no, 1=yes)
        "active": 0          # Not physically active (0=no, 1=yes)
    }
    
    print_data_display("Input Data for Cardiovascular Prediction", {
        "Age": f"{cardio_test_data['age'] / 365.25:.1f} years",
        "Gender": "Male" if cardio_test_data['gender'] == 2 else "Female",
        "Height": f"{cardio_test_data['height']} cm",
        "Weight": f"{cardio_test_data['weight']} kg",
        "BMI": f"{cardio_test_data['weight'] / ((cardio_test_data['height']/100) ** 2):.1f}",
        "Systolic BP": f"{cardio_test_data['ap_hi']} mmHg",
        "Diastolic BP": f"{cardio_test_data['ap_lo']} mmHg",
        "Cholesterol": "Well above normal",
        "Glucose": "Above normal",
        "Smoking": "Yes",
        "Alcohol": "No",
        "Physical Activity": "No"
    })
    
    result = make_api_request("/predict/cardiovascular", cardio_test_data)
    display_prediction_results(result, "Cardiovascular")

def test_diabetes_prediction():
    """Test diabetes risk prediction with sample data"""
    print_separator("DIABETES RISK PREDICTION TEST")
    
    # Sample data for diabetes prediction
    diabetes_test_data = {
        "age": 55.0,                    # Age in years
        "gender": "Male",               # Gender (Female, Male, Other)
        "hypertension": 1,              # Has hypertension (0 or 1)
        "heart_disease": 0,             # No heart disease (0 or 1)
        "smoking_history": "former",    # Former smoker
        "bmi": 28.5,                    # BMI (overweight)
        "HbA1c_level": 6.2,            # HbA1c level (prediabetes range)
        "blood_glucose_level": 110      # Blood glucose level (prediabetes range)
    }
    
    print_data_display("Input Data for Diabetes Prediction", {
        "Age": f"{diabetes_test_data['age']} years",
        "Gender": diabetes_test_data['gender'],
        "Hypertension": "Yes" if diabetes_test_data['hypertension'] else "No",
        "Heart Disease": "Yes" if diabetes_test_data['heart_disease'] else "No",
        "Smoking History": diabetes_test_data['smoking_history'],
        "BMI": f"{diabetes_test_data['bmi']} (Overweight)",
        "HbA1c Level": f"{diabetes_test_data['HbA1c_level']}% (Prediabetes range)",
        "Blood Glucose": f"{diabetes_test_data['blood_glucose_level']} mg/dL (Prediabetes range)"
    })
    
    result = make_api_request("/predict/diabetes", diabetes_test_data)
    display_prediction_results(result, "Diabetes")

def test_cbc_analysis():
    """Test CBC analysis with sample data"""
    print_separator("CBC (COMPLETE BLOOD COUNT) ANALYSIS TEST")
    
    # Sample CBC data
    cbc_test_data = {
        "sex": "male",        # Patient sex
        "wbc": 12.5,          # White Blood Cell count (high)
        "rbc": 4.2,           # Red Blood Cell count (low for male)
        "hemoglobin": 12.0,   # Hemoglobin (low for male)
        "hematocrit": 38,     # Hematocrit (low for male)
        "platelets": 180,     # Platelet count (normal)
        "mcv": 95,            # Mean Corpuscular Volume (normal)
        "mch": 30,            # Mean Corpuscular Hemoglobin (normal)
        "mchc": 34,           # Mean Corpuscular Hemoglobin Concentration (normal)
        "rdw": 13.5           # Red Cell Distribution Width (normal)
    }
    
    print_data_display("Input Data for CBC Analysis", {
        "Patient Sex": cbc_test_data['sex'].title(),
        "WBC (White Blood Cells)": f"{cbc_test_data['wbc']} x10^9/L",
        "RBC (Red Blood Cells)": f"{cbc_test_data['rbc']} x10^12/L",
        "Hemoglobin": f"{cbc_test_data['hemoglobin']} g/dL",
        "Hematocrit": f"{cbc_test_data['hematocrit']}%",
        "Platelets": f"{cbc_test_data['platelets']} x10^9/L",
        "MCV (Mean Corpuscular Volume)": f"{cbc_test_data['mcv']} fL",
        "MCH (Mean Corpuscular Hemoglobin)": f"{cbc_test_data['mch']} pg",
        "MCHC (Mean Corp. Hgb Concentration)": f"{cbc_test_data['mchc']} g/dL",
        "RDW (Red Cell Distribution Width)": f"{cbc_test_data['rdw']}%"
    })
    
    result = make_api_request("/analyze_cbc", cbc_test_data)
    display_cbc_results(result)

def test_model_info():
    """Test model info endpoint"""
    print_separator("MODEL INFORMATION")
    
    try:
        response = requests.get(f"{BASE_URL}/model/info", timeout=10)
        print(f"📡 Model Info Response: {response.status_code}")
        
        if response.status_code == 200:
            info_data = response.json()
            
            print(f"\n🤖 Model Information:")
            print("-" * 60)
            
            # Cardiovascular model info
            cardio_info = info_data.get('cardiovascular_model', {})
            print(f"📊 Cardiovascular Model:")
            print(f"    Loaded: {'✅ Yes' if cardio_info.get('loaded') else '❌ No'}")
            print(f"    Type: {cardio_info.get('type', 'Unknown')}")
            print(f"    Purpose: {cardio_info.get('purpose', 'Unknown')}")
            features = cardio_info.get('features', [])
            if features:
                print(f"    Features: {', '.join(features)}")
            
            # Diabetes model info
            diabetes_info = info_data.get('diabetes_model', {})
            print(f"\n📊 Diabetes Model:")
            print(f"    Loaded: {'✅ Yes' if diabetes_info.get('loaded') else '❌ No'}")
            print(f"    Type: {diabetes_info.get('type', 'Unknown')}")
            print(f"    Purpose: {diabetes_info.get('purpose', 'Unknown')}")
            features = diabetes_info.get('features', [])
            if features:
                print(f"    Features: {', '.join(features)}")
            
            # SHAP info
            shap_info = info_data.get('shap_explanations', 'Not available')
            print(f"\n🔍 SHAP Explanations: {shap_info}")
            
        else:
            print(f"❌ Model info request failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Model info error: {str(e)}")

def run_comprehensive_test():
    """Run all API tests in sequence"""
    print_separator("MEDASSIST API COMPREHENSIVE TEST SUITE")
    print("🧪 This test suite will demonstrate all three API endpoints")
    print("📡 Make sure the API server is running on http://localhost:5001")
    print("\nPress Enter to continue...")
    input()
    
    # Test health endpoint first
    if not test_health_endpoint():
        print("\n❌ API server is not responding. Please start the server first.")
        print("💡 Run: python prediction_api.py")
        return
    
    # Add a small delay between tests
    time.sleep(1)
    
    # Test model info
    test_model_info()
    
    time.sleep(1)
    
    # Test all prediction endpoints
    test_cardiovascular_prediction()
    
    time.sleep(1)
    
    test_diabetes_prediction()
    
    time.sleep(1)
    
    test_cbc_analysis()
    
    print_separator("TEST SUITE COMPLETED")
    print("✅ All API tests have been executed!")
    print("📊 Review the results above to see how each API responds to the sample data.")
    print("\n💡 You can modify the test data in this file to test different scenarios.")

if __name__ == "__main__":
    run_comprehensive_test()
