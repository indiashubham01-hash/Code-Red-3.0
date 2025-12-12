import ollama

question = "what is tract infection?"
response = ollama.chat(model="meditron-7b", messages=[{"role": "user", "content": question}])

print(response['message']['content'])