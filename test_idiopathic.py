import requests
import time

url = "http://127.0.0.1:8003/predict/idiopathic"

data = {
    "age": 65,
    "gender": "Male",
    "smoking_history": "Ever"
}

print(f"Testing {url} with data: {data}")
try:
    # Retry logic since server might be starting
    for i in range(5):
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("Success!")
                print("Response:", response.json())
                break
            else:
                print(f"Failed with code {response.status_code}")
                try:
                    detail = response.json()['detail']
                    print("Error Detail:", detail)
                    with open("test_error.txt", "w") as f:
                        f.write(detail)
                except:
                    print("Raw Response:", response.text)
                    with open("test_error.txt", "w") as f:
                        f.write(response.text)
                break
        except Exception as e:
            print(f"Connection failed (attempt {i+1}): {e}")
            time.sleep(2)
            if i == 4: raise
except Exception as e:
    print(f"Error: {e}")
