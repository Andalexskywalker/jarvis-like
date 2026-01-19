
# tools_registry.py
import inspect
import json

class ToolsRegistry:
    def __init__(self):
        self.tool_map = {}
        self._load_skills()

    def register(self, name, func, description):
        self.tool_map[name] = {
            "func": func,
            "desc": description
        }

    def _load_skills(self):
        """
        Dynamically loads and registers skills. 
        Handles missing dependencies gracefully.
        """
        # Core & Generic Skills
        try:
            from skills import timer, todo, launcher, organizer, creator, voice, system, weather, calc, clock, clipboard, notifications, vision
            self.register("timer.set", timer.set_timer_minutes, "Set a timer for N minutes. Args: minutes (int)")
            self.register("todo.add", todo.handle_todo_add, "Add a task to the todo list. Args: text (str)")
            self.register("todo.show", todo.handle_todo_show, "Show current todos. Args: none")
            self.register("app.open", launcher.handle_open, "Open an app. Args: target (str) e.g. 'notepad', 'youtube'")
            self.register("files.organize", organizer.organize_desktop, "Organize Desktop files into folders. Args: none")
            self.register("files.find", organizer.find_file, "Find a file in User Home. Args: name (str)")
            self.register("files.move", organizer.move_file_custom, "Move a specific file to a folder. Args: file_name (str), target_folder (str)")
            self.register("files.create", creator.create_text_file, "Create a text file. Args: name (str), content (str)")
            self.register("clipboard.read", clipboard.get_clipboard, "Read current clipboard text. Args: none")
            self.register("clipboard.write", clipboard.set_clipboard, "Copy text to clipboard. Args: text (str)")
            self.register("notify.send", notifications.send_notification, "Send a Windows toast notification. Args: message (str), title (str)")
            self.register("vision.capture", vision.capture_screen, "Take a screenshot of the desktop. Args: none")
            self.register("voice.say", voice.speak, "Speak a message out loud. Args: text (str)")
            self.register("system.stats", system.get_system_stats, "Get CPU and RAM usage. Args: none")
            self.register("weather.get", weather.handle_weather, "Get current weather for a city. Args: city (str)")
            self.register("calc.eval", calc.handle_calc, "Evaluate math. Args: expr (str)")
            self.register("clock.time", clock.handle_time, "Get current time. Args: none")
        except ImportError as e:
            print(f"⚠️ Warning: Some core skills failed to load: {e}")

        # Device/Media Skills
        try:
            from skills import media
            self.register("media.volume", media.set_volume, "Set volume. Args: level (int 0-100)")
            self.register("media.mute", media.mute, "Toggle mute.")
            self.register("media.play", media.play_music, "Play music on YouTube. Args: query (str)")
        except ImportError as e:
            print(f"⚠️ Warning: Media skills failed to load: {e}")

    def get_system_prompt_snippet(self):
        """Generates the tool definitions for Friday's system prompt."""
        lines = ["You have access to the following tools. To use one, output ONLY a JSON object like: {\"tool\": \"tool_name\", \"args\": {...}}"]
        for name, data in self.tool_map.items():
            lines.append(f"- {name}: {data['desc']}")
        lines.append("\nIf no tool is needed, just reply with text.")
        return "\n".join(lines)

    def execute(self, tool_name, args_dict):
        """
        Executes a registered tool using dynamic argument mapping (Insepction).
        """
        if tool_name not in self.tool_map:
            return f"Error: Tool '{tool_name}' not found."
        
        try:
            func = self.tool_map[tool_name]["func"]
            sig = inspect.signature(func)
            params = sig.parameters
            
            # Prepare arguments
            call_args = {}
            for name, param in params.items():
                # Direct match
                if name in args_dict:
                    call_args[name] = args_dict[name]
                # Fuzzy match for LLM inconsistencies
                elif name == "minutes" and "time" in args_dict: call_args[name] = args_dict["time"]
                elif name == "target" and "app" in args_dict: call_args[name] = args_dict["app"]
                elif name == "text" and "content" in args_dict: call_args[name] = args_dict["content"]
                elif name == "query" and "name" in args_dict: call_args[name] = args_dict["name"]
                # If only one dict param (Entities pattern), pass the whole dict
                elif len(params) == 1 and (name == "entities" or name == "args"):
                    call_args[name] = args_dict
                elif param.default is not inspect.Parameter.empty:
                    continue # Use default
                else:
                    # Still missing? If first param is dict, try passing everything
                    if len(call_args) == 0 and len(params) == 1:
                        return func(args_dict)

            return func(**call_args) if call_args else func()

        except Exception as e:
            return f"❌ Tool Execution Failed: {type(e).__name__}: {str(e)}"
