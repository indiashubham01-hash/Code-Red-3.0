# Load model directly
from transformers import AutoTokenizer, AutoModelForMaskedLM
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("medicalai/ClinicalBERT")
model = AutoModelForMaskedLM.from_pretrained("medicalai/ClinicalBERT")

# Example usage: Masked language modeling

fill_mask = pipeline("fill-mask", model=model, tokenizer=tokenizer)
result = fill_mask("The patient was prescribed [MASK] for hypertension.")
print(result)