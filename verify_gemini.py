import requests
import json

base_url = "http://127.0.0.1:6969"

def test_report():
    print("\n--- Testing Report Generation ---")
    url = f"{base_url}/generate_report"
    payload = {
        "prediction": {"risk_probability": 0.85, "risk_category": "High"},
        "symptoms": ["chest pain", "shortness of breath"]
    }
    try:
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            print("[SUCCESS] Report Generated:")
            print(res.json()['report'][:200] + "...") # Print first 200 chars
        else:
            print(f"[FAIL] Status: {res.status_code}")
            print(res.text)
    except Exception as e:
        print(f"[ERROR] {e}")

def test_chat():
    print("\n--- Testing AI Assistant (Chat) ---")
    url = f"{base_url}/chat/meditron"
    payload = {
        "message": "What are the symptoms of diabetes?",
        "history": []
    }
    try:
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            print("[SUCCESS] Chat Response:")
            print(res.json()['response'][:200] + "...")
        else:
            print(f"[FAIL] Status: {res.status_code}")
            print(res.text)
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    test_report()
    test_chat()
