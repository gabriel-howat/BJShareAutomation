import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
import os
import sys

def configure(_):
    print("Configuration option selected")

def exit_app(icon, item):
    print("Exiting the application")
    icon.stop()
    sys.exit(0)

def setup_system_tray():
    # Create the system tray icon
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    image_path = os.path.join(parent_dir, "assets", "bj-logo.png")
    image = Image.open(image_path)
    menu = (
        item("Configurações", configure),
        item("Sair", exit_app),
    )
    icon = pystray.Icon("name", image, "BJShareAuto", menu)

    # Start the system tray icon
    thread = threading.Thread(target=icon.run)
    thread.start()

    
#if __name__ == "__main__":
 #   setup_system_tray()