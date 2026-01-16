
import os
import json
import urllib.request

def get_api_key():
    try:
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip()
    except:
        return None

key = get_api_key()
if not key:
    print("No API key found")
    exit(1)

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"

try:
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read().decode())
        print("Writing models to models_list.txt...")
        with open("models_list.txt", "w") as f:
            for m in data.get("models", []):
                if "generateContent" in m.get("supportedGenerationMethods", []):
                    f.write(f"{m['name']}\n")
                    print(f"- {m['name']}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode()}")
except Exception as e:
    print(f"Error listing models: {e}")
