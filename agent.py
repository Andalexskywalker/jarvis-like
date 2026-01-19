
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
        # 1. Update History
        self.history.append(f"User: {user_input}")
        
        # Keep last 6 turns (3 pairs) to avoid token limits
        if len(self.history) > 6:
            self.history = self.history[-6:]
            
        history_text = "\n".join(self.history)

        # 2. Construct Prompt
        system_prompt = (
            "You are Friday, a highly advanced and helpful AI assistant for Windows.\n"
            "You have a warm, professional, and distinctly feminine personality, similar to an intelligent digital companion.\n"
            "ALWAYS prioritize using your tools to help the user. If a tool exists for an action, you MUST use it.\n"
            "When you speak, use the 'voice.say' tool so the user can hear you.\n"
            f"{self.tools.get_system_prompt_snippet()}"
        )
        
        full_prompt = f"{system_prompt}\n\n{history_text}\nAssistant:"

        # 2. Get LLM Decision
        print("Thinking...")
        response_text = self.brain.generate_with_tools(system_prompt, full_prompt, None)
        
        # 3. Detect Tool Calls
        try:
            tools_found = self._extract_json_objects(response_text)
            
            if tools_found:
                results = []
                for tool_data in tools_found:
                    tool_name = tool_data["tool"]
                    args = tool_data.get("args", {})
                    print(f"Executing tool: {tool_name} with {args}")
                    result = self.tools.execute(tool_name, args)
                    results.append(f"Tool '{tool_name}': {result}")
                
                result_msg = "✅ Tasks completed:\n" + "\n".join(results)
                self.history.append(f"Assistant: {result_msg}")
                return result_msg
            
            # If no JSON, just return text
            self.history.append(f"Assistant: {response_text}")
            return response_text

        except Exception as e:
            return f"Error executing tool: {e}\nRaw response: {response_text}"

    def _extract_json_objects(self, text):
        """
        Extracts top-level JSON objects from text using balanced brace counting.
        """
        objs = []
        start_idx = -1
        brace_count = 0
        
        for i, char in enumerate(text):
            if char == '{':
                if brace_count == 0:
                    start_idx = i
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0 and start_idx != -1:
                    json_str = text[start_idx:i+1]
                    try:
                        data = json.loads(json_str)
                        if "tool" in data:
                            objs.append(data)
                    except json.JSONDecodeError:
                        pass
                    start_idx = -1
        return objs

if __name__ == "__main__":
    agent = Agent()
    while True:
        u = input("You: ")
        if u == "exit": break
        print(agent.run(u))
