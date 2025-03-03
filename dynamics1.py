import os
import sys
import django
import time
import threading
from pynput import keyboard, mouse

# Add the parent directory of 'banking_system' to sys.path
sys.path.append('/home/mutabazi/Documents/Projects/banking_system')

# Set the environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')

# Initialize Django
django.setup()

from logger.models import KeystrokeLog, MouseActionLog, BackspaceCount

# Keystroke and mouse dynamics storage
key_press_times = {}
key_release_times = {}
dwell_times = []
flight_times = []
up_down_times = []
backspace_count = 0

mouse_movements = []
click_dynamics = []
path_coordinates = []
mouse_timestamps = []

buffer_lock = threading.Lock()

# Keystroke handling
def on_press(key):
    try:
        key_char = key.char or str(key)
    except AttributeError:
        key_char = str(key)
    with buffer_lock:
        key_press_times[key_char] = time.time()

def on_release(key):
    try:
        key_char = key.char or str(key)
    except AttributeError:
        key_char = str(key)
    with buffer_lock:
        if key_char in key_press_times:
            press_time = key_press_times[key_char]
            release_time = time.time()
            dwell_time = release_time - press_time
            dwell_times.append(dwell_time)

            if key_release_times:
                last_key = list(key_release_times.keys())[-1]
                up_down_time = press_time - key_release_times[last_key]
                up_down_times.append(up_down_time)

                last_release_time = list(key_release_times.values())[-1]
                flight_time = press_time - last_release_time
                flight_times.append(flight_time)

            key_release_times[key_char] = release_time

        if key == keyboard.Key.backspace:
            global backspace_count
            backspace_count += 1

# Mouse handling
def on_move(x, y):
    with buffer_lock:
        timestamp = time.time()
        if path_coordinates:
            last_x, last_y = path_coordinates[-1]
            distance = ((x - last_x) ** 2 + (y - last_y) ** 2) ** 0.5
            time_diff = timestamp - mouse_timestamps[-1]
            speed = distance / time_diff if time_diff > 0 else 0
            mouse_movements.append((distance, speed, timestamp))
        path_coordinates.append((x, y))
        mouse_timestamps.append(timestamp)

def on_click(x, y, button, pressed):
    with buffer_lock:
        action = 'pressed' if pressed else 'released'
        click_dynamics.append({
            'action': action,
            'button': str(button),
            'coordinates': (x, y),
            'timestamp': time.time()
        })

# Display collected metrics
def display_metrics():
    print("\nKeystroke Dynamics Metrics:")
    print(f"Average Dwell Time: {sum(dwell_times) / len(dwell_times) if dwell_times else 0:.4f} seconds")
    print(f"Average Flight Time: {sum(flight_times) / len(flight_times) if flight_times else 0:.4f} seconds")
    print(f"Average Up-Down Time: {sum(up_down_times) / len(up_down_times) if up_down_times else 0:.4f} seconds")
    print(f"Backspace Count: {backspace_count}")

    print("\nMouse Dynamics Metrics:")
    if mouse_movements:
        total_distance = sum([m[0] for m in mouse_movements])
        total_speed = sum([m[1] for m in mouse_movements])
        print(f"Total Movement Distance: {total_distance:.2f} pixels")
        print(f"Average Speed: {total_speed / len(mouse_movements):.2f} pixels per second")
    print(f"Click Dynamics: {len(click_dynamics)} clicks logged")
    print(f"Pointer Path Points: {len(path_coordinates)} points logged")

    log_data()

# Log data into the database
def log_data():
    try:
        for key_char, release_time in key_release_times.items():
            dwell_time = dwell_times.pop(0) if dwell_times else 0
            flight_time = flight_times.pop(0) if flight_times else 0
            up_down_time = up_down_times.pop(0) if up_down_times else 0

            KeystrokeLog.objects.create(
                key=key_char,
                action="release",
                rhythm=0,
                dwell_time=dwell_time,
                flight_time=flight_time,
                up_down_time=up_down_time
            )

        for movement in mouse_movements:
            distance, speed, timestamp = movement
            MouseActionLog.objects.create(
                action="move",
                coordinates="N/A",
                button="N/A",
                distance=distance,
                speed=speed,
                timestamp=timestamp
            )

        for click in click_dynamics:
            MouseActionLog.objects.create(
                action=click['action'],
                coordinates=str(click['coordinates']),
                button=click['button'],
                distance=0,
                speed=0,
                timestamp=click['timestamp']
            )

        BackspaceCount.objects.create(count=backspace_count)
        print("[DEBUG] Data logged successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to log data: {e}")

# Start listeners
def start_listeners():
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)

    keyboard_listener.start()
    mouse_listener.start()

    try:
        keyboard_listener.join()
        mouse_listener.join()
    except KeyboardInterrupt:
        print("\nStopping listeners...")
        display_metrics()

if __name__ == "__main__":
    print("Keystroke and Mouse Dynamics Logger is running. Press Ctrl+C to stop and display metrics.")
    start_listeners()

