import argparse
import os
import sys
import tempfile
from pathlib import Path
from agent import Agent

def check_singleton():
    """Prevents multiple instances of Friday from running."""
    lock_file = Path(tempfile.gettempdir()) / "friday_ai.lock"
    
    if lock_file.exists():
        try:
            # Check if the process in the lock file is still running
            pid = int(lock_file.read_text())
            import psutil
            if psutil.pid_exists(pid):
                print(f"Friday is already running (PID: {pid}). Exiting.")
                sys.exit(0)
        except (ValueError, ImportError, psutil.NoSuchProcess):
            pass # Stale lock or missing psutil, proceed to overwrite
            
    # Create/Update lock file
    lock_file.write_text(str(os.getpid()))
    return lock_file

# Initialize Lock
LOCK = check_singleton()

# Initialize the Brain
print("Initializing AI... (this may take a second)")
jarvis = Agent()

def handle_text(text):
    """
    Routes directly to the AI Agent.
    """
    if not text.strip(): return ""
    return jarvis.run(text)

# -------- UI GRADIO --------
def gradio_app():
    import gradio as gr

    with gr.Blocks(title="Friday AI") as demo:
        gr.Markdown("# Friday AI 👩‍💻\nPowered by Google Gemini")
        chat = gr.Chatbot(height=400)
        inp = gr.Textbox(placeholder="Ask me anything: 'Set timer for 10m', 'Open Notepad'...", lines=1)
        clear = gr.Button("Clear")

        def on_submit(user_msg, history):
            if not user_msg.strip():
                return history, ""
            bot_reply = handle_text(user_msg)
            history = history + [(user_msg, bot_reply)]
            return history, ""

        inp.submit(on_submit, inputs=[inp, chat], outputs=[chat, inp])
        clear.click(lambda: [], outputs=chat)

    demo.launch(server_name="0.0.0.0")

# -------- CLI --------
def cli_loop():
    print("\n------------------------------------------------")
    print("Friday AI Online. 👩‍💻")
    print(f"Model: {jarvis.brain.model_name}")
    print("Type 'exit' to quit.")
    print("------------------------------------------------\n")
    
    while True:
        try:
            text = input("User: ")
        except (EOFError, KeyboardInterrupt):
            break
        if text.strip().lower() in ("exit","quit"):
            break
        
        response = handle_text(text)
        print(f"Friday: {response}\n")

# -------- TRAY MODE --------
def run_tray():
    from skills.ui import TrayApp
    app = TrayApp(jarvis)
    app.run_tray()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Friday AI - Your Desktop Companion")
    parser.add_argument("--ui", action="store_true", help="run Gradio web UI")
    parser.add_argument("--tray", action="store_true", help="run in System Tray (Background)")
    args = parser.parse_args()

    if args.tray:
        run_tray()
    elif args.ui:
        gradio_app()
    else:
        cli_loop()
