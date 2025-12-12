import requests
import json
import time
import sys

def verify():
    url = "http://127.0.0.1:8001/predict"
    try:
        with open("inputs.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("inputs.json not found")
        return

    print(f"Sending request to {url} with data: {data}")
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Success!")
            print("Response:", response.json())
        else:
            print(f"Failed with status code {response.status_code}")
            print("Response:", response.text)
    except requests.exceptions.ConnectionError:
        print("Connection failed. Is the server running?")

if __name__ == "__main__":
    verify()
