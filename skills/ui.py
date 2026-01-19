import tkinter as tk
from tkinter import ttk
import pystray
from PIL import Image, ImageTk
import threading
import os
import time

class TrayApp:
    def __init__(self, agent_instance):
        self.agent = agent_instance
        self.icon_path = "friday_icon.png"
        self.root = None
        self.chat_display = None
        self.entry = None
        self.logo_img = None
        
    def _create_popup(self):
        """Creates the floating, persistent, and sleek chat window."""
        if self.root and self.root.winfo_exists():
            self._toggle_visibility()
            return
            
        self.root = tk.Tk()
        self.root.title("Friday AI")
        self.root.geometry("450x650") # Slightly taller
        self.root.configure(bg="#0f111a") 
        self.root.overrideredirect(True) 
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.94) 
        
        # --- Custom Scrollbar Styling (Modern/Minimalist) ---
        style = ttk.Style()
        style.theme_use('clam')
        
        # Remove arrows by redefining the layout
        style.layout("Midnight.Vertical.TScrollbar", [
            ('Vertical.Scrollbar.trough', {
                'children': [
                    ('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})
                ],
                'sticky': 'ns'
            })
        ])
        
        style.configure("Midnight.Vertical.TScrollbar", 
                        gripcount=0,
                        background="#2a2d3e", 
                        troughcolor="#0f111a", 
                        bordercolor="#0f111a", 
                        lightcolor="#0f111a",  # Remove highlights
                        darkcolor="#0f111a",   # Remove shadows
                        borderwidth=0,
                        arrowsize=0,
                        width=6) # Slimmer
                        
        style.map("Midnight.Vertical.TScrollbar",
                  background=[('active', '#00d4ff'), ('pressed', '#0099bb')])

        # Center on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - 480 
        y = (screen_height // 2) - 325
        self.root.geometry(f"+{x}+{y}")
        
        # Main Container with thin border
        main_frame = tk.Frame(self.root, bg="#0f111a", bd=0, highlightthickness=1, highlightbackground="#1f2233")
        main_frame.pack(fill="both", expand=True)
        
        # Header
        header = tk.Frame(main_frame, bg="#161925", height=55)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Logo Integration
        try:
            pil_img = Image.open(self.icon_path).resize((32, 32), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(pil_img)
            logo_lbl = tk.Label(header, image=self.logo_img, bg="#161925")
            logo_lbl.pack(side="left", padx=(15, 10))
        except Exception as e:
            print(f"UI Logo Error: {e}")
            
        title_lbl = tk.Label(header, text="FRIDAY", fg="#00d4ff", bg="#161925", font=("Segoe UI Semibold", 12, "bold"))
        title_lbl.pack(side="left")
        
        close_btn = tk.Label(header, text="✕", fg="#4a4d6d", bg="#161925", font=("Segoe UI", 14), cursor="hand2")
        close_btn.pack(side="right", padx=15)
        close_btn.bind("<Button-1>", lambda e: self.root.withdraw())
        close_btn.bind("<Enter>", lambda e: close_btn.config(fg="white"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(fg="#4a4d6d"))

        # Chat Area (Custom Scrollbar)
        chat_frame = tk.Frame(main_frame, bg="#0f111a")
        chat_frame.pack(fill="both", expand=True, padx=20, pady=(15, 10))
        
        self.chat_display = tk.Text(
            chat_frame, wrap=tk.WORD, bg="#0f111a", fg="#a0a4b8", 
            font=("Segoe UI", 10), bd=0, highlightthickness=0,
            padx=10, pady=10, insertbackground="#00d4ff"
        )
        
        scrollbar = ttk.Scrollbar(chat_frame, orient="vertical", command=self.chat_display.yview, style="Midnight.Vertical.TScrollbar")
        self.chat_display.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.chat_display.pack(side="left", fill="both", expand=True)
        
        # Styling tags
        self.chat_display.tag_configure("user", foreground="#ffffff", spacing1=5, font=("Segoe UI Semibold", 10))
        self.chat_display.tag_configure("bot", foreground="#00d4ff", spacing1=10)
        self.chat_display.tag_configure("system", foreground="#4a4d6d", font=("Segoe UI Italic", 9))
        self.chat_display.config(state=tk.DISABLED)
        
        # Input Area (Rounded look attempt)
        input_container = tk.Frame(main_frame, bg="#161925", height=70, bd=0)
        input_container.pack(fill="x", side="bottom", padx=20, pady=(0, 20))
        input_container.pack_propagate(False)
        
        inner_input = tk.Frame(input_container, bg="#1c2030", bd=0)
        inner_input.pack(fill="both", expand=True, padx=2, pady=2)

        self.entry = tk.Entry(inner_input, bg="#1c2030", fg="white", insertbackground="#00d4ff",
                         font=("Segoe UI", 11), bd=0, highlightthickness=0)
        self.entry.pack(fill="both", expand=True, padx=15, pady=10)
        self.entry.focus_set()
        
        # Interaction Logic
        def on_submit(event=None):
            query = self.entry.get().strip()
            if query:
                self._update_chat(f"You: {query}", "user")
                self.entry.delete(0, tk.END)
                threading.Thread(target=self._process_query, args=(query,), daemon=True).start()

        self.entry.bind("<Return>", on_submit)
        self.root.bind("<Escape>", lambda e: self.root.withdraw())
        
        # Initial Welcome
        self._update_chat("Friday: Hello, I'm online and ready. How can I assist you?", "bot")
        
        self.root.mainloop()

    def _update_chat(self, text, tag):
        """Safely updates the chat display with tagging."""
        if not self.chat_display: return
        
        def _task():
            # Clean up text to avoid redundant gaps
            clean_text = text.rstrip() + "\n"
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, clean_text, tag)
            self.chat_display.see(tk.END)
            self.chat_display.config(state=tk.DISABLED)
            
        if threading.current_thread() is threading.main_thread():
            _task()
        else:
            self.root.after(0, _task)

    def _process_query(self, query):
        """Hands off the query to the agent and displays results."""
        self._update_chat("Friday is thinking...", "system")
        response = self.agent.run(query)
        self._update_chat(f"Friday: {response}", "bot")

    def _toggle_visibility(self):
        """Shows or hides the window reliably."""
        if not self.root: return
        
        if self.root.state() == "withdrawn":
            self.root.deiconify()
            self.root.lift()
            self.root.attributes("-topmost", True)
            self.root.focus_force() # Force focus
            if self.entry: self.entry.focus_set()
        else:
            self.root.withdraw()

    def run_tray(self):
        """Runs the system tray icon and hotkeys."""
        if not os.path.exists(self.icon_path):
            image = Image.new('RGB', (64, 64), color=(0, 204, 255))
        else:
            image = Image.open(self.icon_path)
            
        menu = pystray.Menu(
            pystray.MenuItem("Ask Friday (Ctrl+Shift+F)", lambda: self._show_popup_thread()),
            pystray.MenuItem("Restart Friday", self._on_restart),
            pystray.MenuItem("Exit", self._on_exit)
        )
        
        # Setup Hotkey
        try:
            import keyboard
            keyboard.add_hotkey('ctrl+shift+f', lambda: self._show_popup_thread())
        except Exception as e:
            print(f"Hotkey Error: {e}")

        self.icon = pystray.Icon("Friday", image, "Friday AI", menu)
        # We need to run the tray in a separate thread so Tkinter can own the main thread if needed
        tray_thread = threading.Thread(target=self.icon.run, daemon=True)
        tray_thread.start()
        
        # Launch UI in main thread
        self._create_popup()

    def _on_restart(self, icon, item):
        """Restarts the application safely on Windows with absolute paths."""
        import sys
        import subprocess
        import os
        import signal
        import tempfile
        from pathlib import Path
        
        try:
            # 1. Prepare fully qualified command
            python = sys.executable
            script = os.path.abspath(sys.argv[0])
            args = sys.argv[1:]
            cmd = [python, script] + args
            
            # 2. Log for debugging
            with open("restart_debug.log", "a") as f:
                f.write(f"[{time.ctime()}] Restart initiated. Cmd: {cmd}\n")
            
            # 3. Aggressive Cleanup (Kill other Fridays)
            try:
                import psutil
                current_pid = os.getpid()
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        # If it's a python process running main.py (and not this one)
                        if "python" in (proc.info['name'] or "").lower():
                            cmdline = proc.info['cmdline'] or []
                            if any("main.py" in arg for arg in cmdline) and proc.info['pid'] != current_pid:
                                proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except ImportError:
                pass 
            
            # 4. Release Singleton Lock (CRITICAL FIX)
            # We must delete the lock file so the new process doesn't think it's a duplicate and exit!
            try:
                lock_file = Path(tempfile.gettempdir()) / "friday_ai.lock"
                if lock_file.exists():
                    lock_file.unlink() # Delete file
                    print("Singleton Lock released for restart.")
            except Exception as e:
                print(f"Failed to release lock: {e}")

            # 5. Cleanup UI
            if self.icon: self.icon.stop()
            if self.root:
                try: self.root.destroy()
                except: pass
            
            # 6. Spawn new process
            subprocess.Popen(cmd, 
                             cwd=os.getcwd(),
                             creationflags=subprocess.CREATE_NO_WINDOW if "pythonw" in python.lower() else 0,
                             close_fds=True)
            
            # 7. Guaranteed exit
            os._exit(0)
        except Exception as e:
            with open("restart_error.log", "a") as f:
                f.write(f"[{time.ctime()}] Restart failed: {e}\n")
            os._exit(1)

    def _show_popup_thread(self):
        """Helper to call toggle from tray thread."""
        if self.root:
            self.root.after(0, self._toggle_visibility)

    def _on_exit(self, icon=None, item=None):
        if self.icon: self.icon.stop()
        if self.root: self.root.quit()
        os._exit(0)
