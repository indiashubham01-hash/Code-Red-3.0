import requests
import json

base_url = "http://127.0.0.1:6969"

def verify_payload(endpoint, data, name):
    print(f"\n--- Testing {name} Payload ({endpoint}) ---")
    print(f"Payload: {json.dumps(data, indent=2)}")
    try:
        res = requests.post(f"{base_url}{endpoint}", json=data)
        if res.status_code == 200:
            print(f"[PASS] Status 200.")
            print(f"Response: {str(res.json())[:200]}...")
        else:
            print(f"[FAIL] Status: {res.status_code}")
            print(res.text)
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    # 1. Diabetes (Full Payload from enhanced form)
    diabetes_data = {
        "age": 55, 
        "gender": "Female", 
        "hypertension": 1, 
        "heart_disease": 1, 
        "smoking_history": "current", 
        "bmi": 32.5, 
        "HbA1c_level": 7.5, 
        "blood_glucose_level": 200
    }
    verify_payload("/predict/diabetes", diabetes_data, "Diabetes Enhanced")

    # 2. CBC (New Module)
    cbc_data = {
        "sex": "female",
        "wbc": 9.2,
        "rbc": 4.1,
        "hemoglobin": 12.5,
        "hematocrit": 38,
        "platelets": 250,
        "mcv": 90,
        "mch": 29,
        "mchc": 33,
        "rdw": 13.0
    }
    verify_payload("/analyze_cbc", cbc_data, "CBC Analysis")
