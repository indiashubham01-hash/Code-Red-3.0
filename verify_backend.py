import requests
import json
import time

BASE_URL = "http://127.0.0.1:8004"

def test_endpoint(name, method, endpoint, data=None):
    print(f"Testing {name} ({endpoint})...")
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        else:
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        
        if response.status_code == 200:
            print(f"PASS: {name}")
            # print(response.json())
        else:
            print(f"FAIL: {name} (Status {response.status_code})")
            print(response.text)
    except Exception as e:
        print(f"ERROR: {name} - {e}")

# Wait for server
print("Waiting for server to be ready...")
for i in range(10):
    try:
        requests.get(f"{BASE_URL}/health")
        break
    except:
        time.sleep(2)

# 1. Health
test_endpoint("Health Check", "GET", "/health")

# 2. Idiopathic (Using clean inputs)
test_endpoint("Idiopathic Model", "POST", "/predict/idiopathic", {
    "age": 65,
    "gender": "Male",
    "smoking_history": "Ever"
})

# 3. ClinicalBERT
test_endpoint("ClinicalBERT", "POST", "/analyze/clinical_bert", {
    "text": "The patient has a history of [MASK] disease."
})

# 4. Cardio NN
test_endpoint("Cardio NN", "POST", "/predict", {
    "age": 20000, "gender": 2, "height": 175, "weight": 75, "ap_hi": 120, "ap_lo": 80, 
    "cholesterol": 1, "gluc": 1, "smoke": 0, "alco": 0, "active": 1
})

print("Verification complete.")
