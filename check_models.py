import os
import requests
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print("Checking available models for your API Key...")


url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    data = response.json()
    
    print("\n✅ You can use the following models:")
    print("-" * 40)
    for model in data.get('models', []):
        
        if 'generateContent' in model.get('supportedGenerationMethods', []):
            print(model['name'])
    print("-" * 40)
except Exception as e:
    print("Error:", e)