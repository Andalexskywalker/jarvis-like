
import os
import json
import time
import urllib.request
import urllib.error

from dotenv import load_dotenv

class LLMClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("❌ Error: GEMINI_API_KEY not found in environment or .env")
            return

        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        print("🧠 Connecting to AI Network...")
        self.model_name = self._resolve_working_model()
        print(f"✅ Connected to: {self.model_name}")
        
        self.url = f"{self.base_url}/{self.model_name}:generateContent?key={self.api_key}"
    
    # _load_env_key is no longer needed

    
    def _resolve_working_model(self):
        candidates = []
        
        # 1. Dynamically fetch available models
        list_url = f"{self.base_url}/models?key={self.api_key}"
        try:
            with urllib.request.urlopen(list_url) as resp:
                data = json.loads(resp.read().decode())
                all_models = [m['name'] for m in data.get("models", [])]
                
                # Priority: Stable Flash -> Stable Pro -> Experimental
                
                # Helper to check if model is "stable" (no 'exp' or 'preview' in name, ideally)
                def is_stable(name):
                    return "exp" not in name and "preview" not in name

                # Filter groups
                stable_flash = [m for m in all_models if "flash" in m and "gemini" in m and is_stable(m)]
                stable_pro = [m for m in all_models if "pro" in m and "gemini" in m and is_stable(m)]
                experimental = [m for m in all_models if ("exp" in m or "preview" in m) and "gemini" in m]
                
                # Sort stable by length (shorter is often the main alias, e.g. gemini-2.0-flash vs gemini-2.0-flash-001)
                stable_flash.sort(key=len)
                stable_pro.sort(key=len)
                
                candidates = stable_flash + stable_pro + experimental
        except Exception as e:
            print(f"⚠️ Model list failed: {e}")
            # Fallback list - Prioritize stable
            candidates = [
                "models/gemini-2.0-flash", 
                "models/gemini-1.5-flash", 
                "models/gemini-1.5-flash-latest",
                "models/gemini-pro"
            ]
        
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
                # 429 means it exists but we have quota issues. 
                if e.code == 429:
                    print(f"⚠️ {model} is rate limited. Skipping...")
                    continue
                # 404 or 400 means problematic.
            except:
                continue
                
        return "models/gemini-2.0-flash" # Ultimate fallback (Stable)

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
        
        # Retry Loop with Exponential Backoff
        max_retries = 5
        base_delay = 5  # Start with 5 seconds
        
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    if "candidates" not in result or not result["candidates"]:
                        return "safe_blocked"
                    return result["candidates"][0]["content"]["parts"][0]["text"]
            
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    wait_time = base_delay * (2 ** attempt)  # 5, 10, 20, 40, 80
                    print(f"⏳ Rate limited. Waiting {wait_time} seconds... (Attempt {attempt+1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                return f"HTTP Error {e.code}: {e.read().decode()}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        return "Error: Rate limit exceeded after multiple retries."
