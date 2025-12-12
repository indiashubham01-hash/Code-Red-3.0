import joblib
import pickle

try:
    encoders = joblib.load("idiopathic_encoders.pkl")
    print("Encoder Classes:")
    print("Sex:", encoders['sex'].classes_)
    print("Smoking:", encoders['smoking'].classes_)
    print("Target:", encoders['target'].classes_)
except Exception as e:
    print(f"Error: {e}")
