# steam_companion_tray.py - Shows icon in system tray
import pystray
from PIL import Image
import threading

def create_icon():
    # Create tray icon
    image = Image.new('RGB', (64, 64), (40, 44, 52))
    icon = pystray.Icon("steam_companion", image, "Steam AI Companion")
    icon.menu = pystray.Menu(
        pystray.MenuItem("Show Log", show_log),
        pystray.MenuItem("Exit", exit_app)
    )
    return icon

# Runs in system tray - click icon to control