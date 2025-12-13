import requests
import json

url = "http://127.0.0.1:6969/generate_report"

payload = {
    "prediction": {
        "risk_probability": 0.75,
        "risk_category": "High",
        "prediction": 1
    },
    "symptoms": ["Fatigue", "Chest Pain"]
}

try:
    print("Sending request to /generate_report...")
    res = requests.post(url, json=payload)
    print(f"Status: {res.status_code}")
    print(f"Headers: {res.headers}")
    if res.status_code == 200:
        print("Success!")
        print(res.json()['report'])
    else:
        print(f"Failed: {res.status_code}")
        print(res.text)
except Exception as e:
    print(f"Error: {e}")
