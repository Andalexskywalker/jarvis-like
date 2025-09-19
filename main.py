# main.py
from nlu import parse_intent
from skills import todo, timer
import gradio as gr

def handle_text(text):
    parsed = parse_intent(text)
    intent = parsed["intent"]
    ent = parsed["entities"]
    if intent == "todo.add":
        return todo.handle_todo_add(ent)
    if intent == "todo.show":
        return todo.handle_todo_show(ent)
    if intent == "timer.set_minutes":
        return timer.set_timer_minutes(ent["minutes"])
    if intent == "timer.set_seconds":
        return timer.set_timer_seconds(ent["seconds"])
    if intent == "smalltalk.greet":
        return "Hey — what would you like to do? You can say 'add buy milk' or 'set timer 10m'."
    return "Sorry, I didn't get that. Try: 'add buy milk' or 'show todos' or 'set timer 5m'."

# minimal CLI:
if __name__ == "__main__":
    print("Jarvis-lite (text mode). Type 'exit' to quit.")
    while True:
        text = input("> ")
        if text.strip().lower() in ("exit","quit"):
            break
        out = handle_text(text)
        print(out)

# optional: Gradio UI (uncomment to run)
# def gradio_app():
#     with gr.Blocks() as demo:
#         txt = gr.Textbox(placeholder="Type a command", lines=1)
#         out = gr.Textbox(label="Assistant")
#         txt.submit(lambda v: handle_text(v), inputs=txt, outputs=out)
#     demo.launch()
#
# if you want a phone-friendly UI, run gradio_app()
