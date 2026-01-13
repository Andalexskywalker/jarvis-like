
# agent.py
import json
import re
from llm_client import LLMClient
from tools_registry import ToolsRegistry

class Agent:
    def __init__(self):
        self.brain = LLMClient()
        self.tools = ToolsRegistry()
        self.history = [] # Keep short context or implement sliding window

    def run(self, user_input):
        # 1. Construct Prompt
        system_prompt = (
            "You are Friday, a helpful and intelligent desktop assistant.\n"
            "You have a warm, professional, and feminine personality.\n"
            "You can execute Python functions to help the user.\n"
            f"{self.tools.get_system_prompt_snippet()}"
        )
        
        # Add to history
        full_prompt = f"{system_prompt}\n\nUser: {user_input}\nAssistant:"

        # 2. Get LLM Decision
        print("Thinking...")
        response_text = self.brain.generate_with_tools(system_prompt, full_prompt, None)
        
        # 3. Detect Tool Call (JSON)
        # We look for a JSON object in the response
        try:
            # Greedy regex to find the first JSON-like object
            match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if match:
                json_str = match.group(0)
                data = json.loads(json_str)
                
                if "tool" in data:
                    tool_name = data["tool"]
                    args = data.get("args", {})
                    
                    print(f"Executing tool: {tool_name} with {args}")
                    result = self.tools.execute(tool_name, args)
                    
                    return f"✅ Done! ({result})"
            
            # If no JSON, just return text
            return response_text

        except Exception as e:
            return f"Error executing tool: {e}\nRaw response: {response_text}"

if __name__ == "__main__":
    agent = Agent()
    while True:
        u = input("You: ")
        if u == "exit": break
        print(agent.run(u))
