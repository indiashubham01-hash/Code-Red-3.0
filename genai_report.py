import os
try:
    import google.generativeai as genai
except ImportError:
    genai = None
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY and genai:
    # Warning: Using a dummy key "dummy_key_12345" will cause API calls to fail if not replaced with a real key.
    # The user asked for a dummy key, so we proceed, but real generation requires a valid key.
    genai.configure(api_key=GEMINI_API_KEY)

def generate_medical_report(prediction_data, symptoms):
    """
    Generates a medical report using Gemini based on prediction data and symptoms.
    """
    if genai is None or not GEMINI_API_KEY or "dummy" in GEMINI_API_KEY:
        # Mock response for dummy key to ensure "presentable report" without crashing
        return f"""
        **Medical Analysis Report**
        
        **Summary of Findings:**
        Based on the provided data ({prediction_data.get('risk_category', 'Analysis')}), there are indicators that suggest attention is needed. The AI model estimates a risk probability of {prediction_data.get('risk_probability', 0)*100:.1f}%.
        
        **Symptoms Noted:**
        {', '.join(symptoms) if symptoms else 'None reported'}
        
        **Recommendations:**
        1. Consult a healthcare provider for a comprehensive evaluation.
        2. Monitor lifestyle factors such as diet and exercise.
        3. Regular check-ups are advised.
        
        *Disclaimer: This report is a simulation (Dummy API Key).*
        """

    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    You are a medical AI assistant. Generate a professional, empathetic, and concise medical report for a patient based on the following analysis.
    
    Patient Data: {prediction_data}
    Reported Symptoms: {symptoms}
    
    The report should include:
    1. Summary of Findings
    2. Potential Causes (based on data)
    3. Recommended Next Steps (Lifestyle, Tests, Doctor Visit)
    
    Disclaimer: This is AI-generated and not a substitute for professional medical advice.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating report: {str(e)}"
