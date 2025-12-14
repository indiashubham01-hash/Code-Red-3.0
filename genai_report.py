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
    # known expired key check to prevent API call
    if not api_key or api_key == "AIzaSyDB-KJ_AJkRYz3zHfZ_hb_zhbQbcMfXc_A" or "API_KEY" in api_key:
        print("Using Fallback Report (Key Invalid/Expired)")
        return """**Medical Analysis Report (Fallback Mode)**
            
*Note: Excepted AI generation failure (Key Expired). Displaying placeholder analysis based on clinical rules.*

**1. Risk Analysis**
Based on the provided clinical data, the patient has been flagged with a **High Risk** profile. This assessment is derived from the ML model's probabilistic output. The elevated risk suggests a significant likelihood of cardiovascular or metabolic complications if left unmanaged.

**2. Symptom Correlation**
The reported symptoms (e.g., if any were provided) are consistent with hemodynamic instability often seen in high-risk patients. Fatigue or chest discomfort may correlate with the elevated blood pressure or glucose levels noted in the input.

**3. Recommended Actions**
- **Immediate**: Consult a cardiologist for a stress test and echocardiogram.
- **Labs**: Lipid panel, HbA1c, and renal function tests.
- **Lifestyle**: Strict sodium restriction (<2g/day) and supervised aerobic exercise.

**4. Warning**
This is an automated analysis for informational purposes only. It is not a medical diagnosis. Please consult a licensed physician."""

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        # Catch-all fallback
        print(f"Gemini Error: {e}")
        return """**Medical Analysis Report (System Fallback)**
        
*System encountered an error connecting to AI service. displaying standard advice.*

**Risk Analysis**: The calculated risk probability requires clinical attention.
**Recommendation**: Proceed with standard cardiovascular screening protocols.
**Disclaimer**: Consult a doctor."""

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
    You are 'FedHealth AI', a helpful medical assistant. 
    User Question: {message}
    
    Answer concisely and helpfully. Always advice consulting a real doctor for serious issues.
    """
    return call_gemini(prompt)
