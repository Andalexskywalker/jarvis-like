# main.py
from nlu import parse_intent
from skills import todo, timer

def handle_text(text):
    parsed = parse_intent(text)
    intent = parsed["intent"]; ent = parsed["entities"]
    if intent == "todo.add":
        return todo.handle_todo_add(ent)
    if intent == "todo.show":
        return todo.handle_todo_show(ent)
    if intent == "timer.set_minutes":
        return timer.set_timer_minutes(ent["minutes"])
    if intent == "timer.set_seconds":
        return timer.set_timer_seconds(ent["seconds"])
    if intent == "smalltalk.greet":
        return "Hey — try 'add buy milk', 'show todos', or 'set timer 5m'."
    return "Sorry, I didn't get that. Try: 'add buy milk' / 'show todos' / 'set timer 5m'."

# -------- UI GRADIO --------
def gradio_app():
    import gradio as gr

    with gr.Blocks(title="Jarvis-Like") as demo:
        gr.Markdown("# Jarvis-Like 🗣️🤖\nType a command below.")
        inp = gr.Textbox(lines=1, placeholder="e.g., add buy milk / show todos / set timer 1m")
        out = gr.Textbox(label="Assistant")

        def on_submit(txt):
            return handle_text(txt)

        inp.submit(on_submit, inputs=inp, outputs=out)
        gr.Button("Send").click(on_submit, inputs=inp, outputs=out)

    # LAN: demo.launch(server_name="0.0.0.0")  # abre na rede local (telemóvel)
    demo.launch()  # só no teu PC por defeito

# -------- CLI --------
def cli_loop():
    print("Jarvis-like (text mode). Type 'exit' to quit.")
    while True:
        try:
            text = input("> ")
        except (EOFError, KeyboardInterrupt):
            break
        if text.strip().lower() in ("exit","quit"):
            break
        print(handle_text(text))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ui", action="store_true", help="run Gradio web UI")
    parser.add_argument("--lan", action="store_true", help="expose UI on LAN")
    args = parser.parse_args()

    if args.ui:
        if args.lan:
            # lança na rede local (telemóvel no mesmo Wi-Fi)
            import gradio as gr
            gr.set_static_paths([])  # opcional, só para evitar avisos
            # re-lança com server_name
            import gradio as gr
            with gr.Blocks() as empty: pass
            # chamamos a função normal mas ajustamos launch abaixo:
        # chamar a app mas ajustando o launch:
        import gradio as gr
        with gr.Blocks() as _tmp: pass
        # hack simples: re-lançar com parâmetros
        # mais fácil: chamar diretamente:
        if args.lan:
            # reimplement launch com LAN
            import gradio as gr
            def launch_lan():
                import gradio as gr
                with gr.Blocks(title="Jarvis-Like") as demo:
                    gr.Markdown("# Jarvis-Like 🗣️🤖\nType a command below.")
                    inp = gr.Textbox(lines=1, placeholder="e.g., add buy milk / show todos / set timer 1m")
                    out = gr.Textbox(label="Assistant")
                    inp.submit(lambda t: handle_text(t), inputs=inp, outputs=out)
                    gr.Button("Send").click(lambda t: handle_text(t), inputs=inp, outputs=out)
                demo.launch(server_name="0.0.0.0", server_port=7860)
            launch_lan()
        else:
            gradio_app()
    else:
        cli_loop()
