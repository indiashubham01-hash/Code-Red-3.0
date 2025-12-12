import requests
import json

BASE_URL = "http://127.0.0.1:8001"

def test_health():
    print("Testing /health...")
    try:
        r = requests.get(f"{BASE_URL}/health")
        print(json.dumps(r.json(), indent=2))
    except Exception as e:
        print(f"Health check failed: {e}")

def test_diabetes():
    print("\nTesting /predict/diabetes...")
    payload = {
        "age": 45,
        "gender": "Male",
        "hypertension": 1,
        "heart_disease": 0,
        "smoking_history": "former",
        "bmi": 28.5,
        "HbA1c_level": 6.2,
        "blood_glucose_level": 140
    }
    try:
        r = requests.post(f"{BASE_URL}/predict/diabetes", json=payload)
        if r.status_code == 200:
            print("Success!")
            # parse specific keys to avoid flooding console with SHAP
            res = r.json()
            print(f"Prediction: {res['prediction']}")
            print(f"Risk Prob: {res['risk_probability']}")
            print(f"SHAP Summary: {res['explanations']['summary']}")
        else:
            print(f"Failed: {r.text}")
    except Exception as e:
        print(f"Diabetes test failed: {e}")

def test_cardio_xgb():
    print("\nTesting /predict/cardiovascular (XGBoost)...")
    payload = {
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
    try:
        r = requests.post(f"{BASE_URL}/predict/cardiovascular", json=payload)
        if r.status_code == 200:
            print("Success!")
            res = r.json()
            print(f"Prediction: {res['prediction']}")
            print(f"Risk Prob: {res['risk_probability']}")
            print(f"SHAP Summary: {res['explanations']['summary']}")
        else:
            print(f"Failed: {r.text}")
    except Exception as e:
        print(f"Cardio XGB test failed: {e}")

if __name__ == "__main__":
    test_health()
    test_diabetes()
    test_cardio_xgb()
