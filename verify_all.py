import requests
import json

base_url = "http://127.0.0.1:6969"

def verify_post(endpoint, data, name):
    print(f"\n--- Testing {name} ({endpoint}) ---")
    try:
        res = requests.post(f"{base_url}{endpoint}", json=data)
        if res.status_code == 200:
            print(f"[PASS] Status 200. Response subset: {str(res.json())[:100]}")
        else:
            print(f"[FAIL] Status: {res.status_code}")
            print(res.text[:200])
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    # Diabetes
    verify_post(
        "/predict/diabetes",
        {
            "age": 45, "gender": "Male", "hypertension": 1, "heart_disease": 0,
            "smoking_history": "former", "bmi": 28.5, "HbA1c_level": 6.2, "blood_glucose_level": 140
        },
        "Diabetes"
    )

    # Idiopathic
    verify_post(
        "/predict/idiopathic",
        {"age": 65, "gender": "Male", "smoking_history": "Ever"},
        "Idiopathic"
    )

    # Chat (Gemini)
    verify_post(
        "/chat/meditron",
        {"message": "Hello AI", "history": []},
        "Chat"
    )

    # Report (Gemini)
    verify_post(
        "/generate_report",
        {"prediction": {"risk": "High"}, "symptoms": ["pain"]},
        "Report"
    )
