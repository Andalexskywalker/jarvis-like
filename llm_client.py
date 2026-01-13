
import os
import json
import time
import urllib.request
import urllib.error

class LLMClient:
    def __init__(self):
        self.api_key = self._load_env_key()
        if not self.api_key:
            print("❌ Error: GEMINI_API_KEY not found in .env")
            return

        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        print("🧠 Connecting to AI Network...")
        self.model_name = self._resolve_working_model()
        print(f"✅ Connected to: {self.model_name}")
        
        self.url = f"{self.base_url}/{self.model_name}:generateContent?key={self.api_key}"

    def _load_env_key(self):
        try:
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        return line.split("=", 1)[1].strip()
        except:
            return None
    
    def _resolve_working_model(self):
        candidates = []
        
        # 1. Dynamically fetch available models
        list_url = f"{self.base_url}/models?key={self.api_key}"
        try:
            with urllib.request.urlopen(list_url) as resp:
                data = json.loads(resp.read().decode())
                all_models = [m['name'] for m in data.get("models", [])]
                
                # Priority: Flash -> Pro
                flash_models = [m for m in all_models if "flash" in m and "gemini" in m]
                pro_models = [m for m in all_models if "pro" in m and "gemini" in m]
                
                # Sort to prefer shorter names (usually stable aliases) or specific versions?
                # Actually, let's just try them all.
                candidates = flash_models + pro_models
        except Exception as e:
            print(f"⚠️ Model list failed: {e}")
            candidates = ["models/gemini-1.5-flash", "models/gemini-pro"]

        # 2. Test candidates
        for model in candidates:
            # print(f"Testing {model}...") 
            test_url = f"{self.base_url}/{model}:generateContent?key={self.api_key}"
            payload = json.dumps({"contents": [{"parts": [{"text": "hi"}]}]}).encode("utf-8")
            req = urllib.request.Request(test_url, data=payload, headers={"Content-Type": "application/json"})
            
            try:
                urllib.request.urlopen(req)
                return model
            except urllib.error.HTTPError as e:
                # 429 means it exists and we have quota issues (so it's valid, we just need to wait)
                if e.code == 429:
                    return model
                # 404 or 400 means problematic.
            except:
                continue
                
        return "models/gemini-1.5-flash" # Ultimate fallback

    def generate_with_tools(self, system_instruction, prompt, tools_schema=None):
        if not self.api_key: return "Error: No API Key."

        payload = {
            "contents": [{
                "parts": [{"text": system_instruction + "\n\n" + prompt}]
            }]
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.url, 
            data=data, 
            headers={"Content-Type": "application/json"}
        )
        
        # Retry Loop
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    if "candidates" not in result or not result["candidates"]:
                        return "safe_blocked"
                    return result["candidates"][0]["content"]["parts"][0]["text"]
            
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    print(f"⏳ Rate limited. Waiting 20 seconds... (Attempt {attempt+1}/{max_retries})")
                    time.sleep(20)
                    continue
                return f"HTTP Error {e.code}: {e.read().decode()}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        return "Error: Rate limit exceeded."
