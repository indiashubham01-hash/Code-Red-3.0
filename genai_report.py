import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Fetch Key from Environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def call_gemini(prompt):
    """
    Calls the Gemini API using the official google-genai SDK.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY not found. Ensure load_dotenv() is called."
    
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Request Failed: {str(e)}"

def generate_medical_report(prediction, symptoms):
    prompt = f"""
    Act as a Board-Certified Cardiologist. Analyze the following patient data for a medical report:
    
    Patient Risk Assessment: {prediction}
    Reported Symptoms: {symptoms}
    
    Please structure your response as a formal Medical Analysis Report:
    1. **Risk Analysis**: Interpret the prediction probability and category.
    2. **Symptom Correlation**: Explain how the symptoms might relate to the risk.
    3. **Recommended Actions**: Specific medical tests (e.g., ECG, Lipid Profile), lifestyle modifications.
    4. **Warning**: Include a standard medical disclaimer.
    """
    return call_gemini(prompt)

def generate_chat_response(message):
    prompt = f"""
    You are 'MedAssist AI', a helpful medical assistant. 
    User Question: {message}
    
    Answer concisely and helpfully. Always advice consulting a real doctor for serious issues.
    """
    return call_gemini(prompt)
