import joblib
import sys

print("Loading encoders...")
try:
    encoders = joblib.load("idiopathic_encoders.pkl")
except Exception as e:
    print(f"Failed to load pickle: {e}")
    sys.exit(1)

print("Encoders loaded.")

# Sex Test
sex_val = "male" # The cleaned value in app.py
try:
    print(f"Testing Sex: '{sex_val}'")
    classes = encoders['sex'].classes_
    print(f"Known classes: {classes}")
    res = encoders['sex'].transform([sex_val])
    print(f"Success: {res}")
except Exception as e:
    print(f"FAIL Sex: {e}")

# Smoking Test
smoke_val = "Ever" # The cleaned value in app.py
try:
    print(f"Testing Smoking: '{smoke_val}'")
    classes = encoders['smoking'].classes_
    print(f"Known classes: {classes}")
    res = encoders['smoking'].transform([smoke_val])
    print(f"Success: {res}")
except Exception as e:
    print(f"FAIL Smoking: {e}")
