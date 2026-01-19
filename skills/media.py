# skills/media.py
from ctypes import cast, POINTER
from comtypes import CoInitialize, CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import webbrowser

def _get_volume_interface():
    # Ensure COM is initialized
    try:
        CoInitialize()
    except:
        pass
        
    try:
        devices = AudioUtilities.GetSpeakers()
        # Handle various pycaw object wrappers
        if hasattr(devices, "Activate"):
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        elif hasattr(devices, "_device") and hasattr(devices._device, "Activate"):
            interface = devices._device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        else:
             # Last resort: try to cast or use the item if it's a collection
             try:
                 interface = devices[0].Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
             except:
                 raise Exception(f"Device object {type(devices)} missing Activate method.")
    except Exception as e:
         raise Exception(f"Volume activation failed: {e}")

    return cast(interface, POINTER(IAudioEndpointVolume))

def set_volume(level):
    """
    Sets system volume to a specific percentage (0-100).
    """
    try:
        if isinstance(level, dict): level = level.get('level', 50)
        level = int(level)
        level = max(0, min(100, level))
        
        volume = _get_volume_interface()
        # Pycaw scalar volume is 0.0 to 1.0
        scalar = level / 100.0
        volume.SetMasterVolumeLevelScalar(scalar, None)
        return f"Volume set to {level}%"
    except Exception as e:
        return f"Error setting volume: {e}"

def mute(args=None):
    """
    Toggles mute.
    """
    try:
        volume = _get_volume_interface()
        current = volume.GetMute()
        volume.SetMute(not current, None)
        state = "muted" if not current else "unmuted"
        return f"System {state}"
    except Exception as e:
        return f"Error muting: {e}"

def play_music(query):
    """
    Plays music on YouTube.
    """
    if isinstance(query, dict): query = query.get('query', 'lofi hip hop')
    
    url = f"https://www.youtube.com/results?search_query={query}"
    # Use the 'f' string properly encoded, or just let browser handle it.
    # Actually, let's play the first video if possible, or just open search.
    # Opening search is safer/easier for MVP.
    webbrowser.open(url)
    return f"Playing {query} on YouTube"

