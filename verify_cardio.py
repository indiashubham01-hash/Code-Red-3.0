import requests
import json

url = "http://127.0.0.1:6969/predict/cardiovascular"

payload = {
  "age": 20000,
  "gender": 1,
  "height": 175,
  "weight": 70,
  "ap_hi": 120,
  "ap_lo": 80,
  "cholesterol": 1,
  "gluc": 1,
  "smoke": 0,
  "alco": 0,
  "active": 1
}

try:
    print(f"Sending request to {url}...")
    res = requests.post(url, json=payload)
    print(f"Status: {res.status_code}")
    if res.status_code == 200:
        print("Success! Response:")
        print(json.dumps(res.json(), indent=2))
        if res.json().get('explanations') is None:
            print("[INFO] Explanations are None, indicating Fallback NN was used.")
    else:
        print("Failed.")
        print(res.text)
except Exception as e:
    print(f"Error: {e}")
