# skills/vision.py
from PIL import ImageGrab
import os

def capture_screen(_entities=None):
    """
    Takes a screenshot of the main display and saves it.
    Returns the path to the saved image.
    """
    try:
        # Create a screenshots folder if it doesn't exist
        save_dir = "screenshots"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        filename = f"screenshot_{int(os.path.getmtime('.'))}.png"
        save_path = os.path.join(save_dir, filename)
        
        screenshot = ImageGrab.grab()
        screenshot.save(save_path)
        
        return f"Screenshot captured and saved to: {save_path}"
    except Exception as e:
        return f"Failed to capture screen: {e}"
