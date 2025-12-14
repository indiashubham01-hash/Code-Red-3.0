import requests
import json
import socket

# Try to detect port (defaulting to 6969 as per recent changes)
PORT = 6969
BASE_URL = f"http://127.0.0.1:{PORT}"

def check_backend():
    print(f"Checking backend at {BASE_URL}...")
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=2)
        print(f"Health Check: {resp.status_code}")
        print(resp.json())
        return True
    except Exception as e:
        print(f"Health Check Failed: {e}")
        return False

def test_prediction():
    url = f"{BASE_URL}/predict/cardiovascular/result"
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
    print(f"\nTesting Prediction: {url}")
    try:
        resp = requests.post(url, json=payload, timeout=5)
        print(f"Status: {resp.status_code}")
        if resp.status_code != 200:
            print("Response Text:")
            print(resp.text)
        else:
            print("Success Response:")
            print(resp.json())
    except Exception as e:
        print(f"Prediction Request Failed: {e}")

if __name__ == "__main__":
    if check_backend():
        test_prediction()
    else:
        print("\nBackend seems down. Please ensure 'python app.py' is running.")
