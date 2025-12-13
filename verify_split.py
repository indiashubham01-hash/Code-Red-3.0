import requests
import json

base_url = "http://127.0.0.1:6969"

def test_split_endpoints():
    print("\n--- Testing Split Cardio Endpoints ---")
    payload = {
      "age": 20000, "gender": 1, "height": 165, "weight": 68, 
      "ap_hi": 120, "ap_lo": 80, "cholesterol": 1, "gluc": 1, 
      "smoke": 0, "alco": 0, "active": 1
    }
    
    # 1. Result Endpoint
    print("\nCalling /predict/cardiovascular/result...")
    try:
        res1 = requests.post(f"{base_url}/predict/cardiovascular/result", json=payload)
        if res1.status_code == 200:
            print(f"[PASS] Result: {res1.json()}")
        else:
            print(f"[FAIL] Result Status: {res1.status_code}")
            print(res1.text)
    except Exception as e: print(f"[ERROR] Result: {e}")

    # 2. Explanation Endpoint
    print("\nCalling /predict/cardiovascular/explanation...")
    try:
        res2 = requests.post(f"{base_url}/predict/cardiovascular/explanation", json=payload)
        if res2.status_code == 200:
            print(f"[PASS] Explanation: {res2.json()}")
        else:
            print(f"[FAIL] Explanation Status: {res2.status_code}")
            print(res2.text)
    except Exception as e: print(f"[ERROR] Explanation: {e}")

if __name__ == "__main__":
    test_split_endpoints()
