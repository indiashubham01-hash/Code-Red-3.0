import requests
import json

base_url = "http://127.0.0.1:6969"

def check_cardio():
    print("\n--- Testing Cardio Endpoint ---")
    url = f"{base_url}/predict/cardiovascular/result"
    payload = {
        "age": 18000, "gender": 1, "height": 170, "weight": 70, "ap_hi": 120, "ap_lo": 80,
        "cholesterol": 1, "gluc": 1, "smoke": 0, "alco": 0, "active": 1
    }
    try:
        res = requests.post(url, json=payload)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.json()}")
    except Exception as e:
        print(f"Error: {e}")

def check_diabetes():
    print("\n--- Testing Diabetes Endpoint ---")
    url = f"{base_url}/predict/diabetes"
    payload = {
        "age": 45, "gender": "Male", "hypertension": 0, "heart_disease": 0, 
        "smoking_history": "never", "bmi": 25.0, "HbA1c_level": 5.5, 
        "blood_glucose_level": 100
    }
    try:
        res = requests.post(url, json=payload)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_cardio()
    check_diabetes()
