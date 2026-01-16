
# tools_registry.py
import inspect


class ToolsRegistry:
    def __init__(self):
        self.tool_map = {}
        
        # Robust Skills Loading
        # 1. System / Core (Usually safe)
        try:
            from skills import timer, todo, launcher, organizer
            self.register("timer.set", timer.set_timer_minutes, "Set a timer for N minutes. Args: minutes (int)")
            self.register("todo.add", todo.handle_todo_add, "Add a task to the todo list. Args: text (str)")
            self.register("todo.show", todo.handle_todo_show, "Show current todos. Args: none")
            self.register("app.open", launcher.handle_open, "Open an app. Args: target (str) e.g. 'notepad', 'youtube'")
            self.register("files.organize", organizer.organize_desktop, "Organize Desktop files into folders. Args: none")
            self.register("files.find", organizer.find_file, "Find a file in User Home. Args: name (str)")
        except ImportError as e:
            print(f"⚠️ Warning: Core skills failed to load: {e}")

        # 2. Weather (Requires requests?)
        try:
            from skills import weather
            self.register("weather.get", weather.handle_weather, "Get weather. Args: city (str)")
        except ImportError as e:
             print(f"⚠️ Warning: Weather skill failed to load: {e}")

        # 3. Media (Requires comtypes/pycaw - PROBABLY FLAKY)
        try:
            from skills import media
            
            # Media Tools
            self.register("media.volume", media.set_volume, "Set volume percentage. Args: level (int 0-100)")
            self.register("media.mute", media.mute, "Mute/Unmute system audio.")
            self.register("media.play", media.play_music, "Search and play music on YouTube. Args: query (str)")
        except ImportError as e:
            print(f"⚠️ Warning: Media skills (volume/music) failed to load: {e}")

    def register(self, name, func, description):
        self.tool_map[name] = {
            "func": func,
            "desc": description
        }

    def get_system_prompt_snippet(self):
        """
        Generates the JSON schema part of the system prompt
        """
        lines = ["You have access to the following tools. To use one, output ONLY a JSON object like: {\"tool\": \"tool_name\", \"args\": {...}}"]
        for name, data in self.tool_map.items():
            lines.append(f"- {name}: {data['desc']}")
        
        lines.append("If no tool is needed, just reply with text.")
        return "\n".join(lines)

    def execute(self, tool_name, args_dict):
        if tool_name not in self.tool_map:
            return f"Error: Tool '{tool_name}' not found."
        
        func = self.tool_map[tool_name]["func"]
        
        # Simple argument mapping
        # In a robust system, we would inspect signature and bind args
        # Here we just pass what we know depends on the simple skills signature
        try:
            # Inspection specific to the user's legacy 'skills' which often take a single dict or arg
            # We adapt based on the known signatures from reading 'main.py' earlier
            
            if tool_name == "todo.add":
                return func({"text": args_dict.get("text")}) 
            elif tool_name == "todo.show":
                return func({})
            elif tool_name == "timer.set":
                return func(int(args_dict.get("minutes", 0)))
            elif tool_name == "weather.get":
               return func({"city": args_dict.get("city")})
            elif tool_name == "app.open":
               return func({"target": args_dict.get("target")})
            
            # Media Dispatch
            elif tool_name == "media.volume":
                return func(args_dict.get("level", 50))
            elif tool_name == "media.mute":
                return func()
            elif tool_name == "media.play":
                return func(args_dict.get("query", ""))

            # Organizer Dispatch
            elif tool_name == "files.organize":
                return func()
            elif tool_name == "files.find":
                return func(args_dict.get("name", ""))
            
            return "Tool executed but no adapter found."
        except Exception as e:
            return f"Execution Error: {str(e)}"
