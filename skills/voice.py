# skills/voice.py
import pyttsx3
import threading

def speak(text):
    """
    Makes Friday speak. Running in a separate thread to avoid blocking.
    """
    if isinstance(text, dict): text = text.get("text", "")
    
    def _speak_thread():
        try:
            import comtypes
            comtypes.CoInitialize()
            engine = pyttsx3.init()
            
            voices = engine.getProperty('voices')
            # Look for Zira or any voice with "female" or "zira" in it
            target_voice = None
            for v in voices:
                if "zira" in v.name.lower() or "female" in v.name.lower() or "hazel" in v.name.lower():
                    target_voice = v.id
                    break
            
            if target_voice:
                engine.setProperty('voice', target_voice)
            elif len(voices) > 1:
                engine.setProperty('voice', voices[1].id)
            
            engine.setProperty('rate', 180) 
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Voice Error: {e}")
        finally:
            try:
                comtypes.CoUninitialize()
            except:
                pass

    threading.Thread(target=_speak_thread, daemon=True).start()
    return f"Speaking: \"{text}\""
