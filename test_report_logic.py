import sys
from unittest.mock import MagicMock

# Mock google.generativeai
sys.modules["google"] = MagicMock()
sys.modules["google.generativeai"] = MagicMock()

# Now import the report script
from genai_report import generate_medical_report

# Test Data
prediction = {'risk_probability': 0.85, 'risk_category': 'High'}
symptoms = ['Shortness of Breath', 'Palpitations']

print("Testing Report Generation...")
report = generate_medical_report(prediction, symptoms)
print("\nGenerated Report:")
print(report)

if "Medical Analysis Report" in report and "Shortness of Breath" in report:
    print("\n[PASS] logic verified.")
else:
    print("\n[FAIL] report content mismatch.")
