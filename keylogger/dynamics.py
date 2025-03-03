import time
import threading
from pynput import keyboard, mouse

# Keystroke and mouse dynamics storage
key_press_times = {}  # Store key press times
key_release_times = {}  # Store key release times
dwell_times = []  # Hold times
flight_times = []  # Down-Down times
up_down_times = []  # Up-Down times
backspace_count = 0  # Count of backspaces

# Mouse movement and click dynamics
mouse_movements = []
click_dynamics = []
path_coordinates = []
mouse_timestamps = []  # To track movement timestamps

buffer_lock = threading.Lock()

# Calculate metrics on key press
def on_press(key):
    global key_press_times
    try:
        key_char = key.char
    except AttributeError:
        key_char = str(key)

    with buffer_lock:
        key_press_times[key_char] = time.time()

# Calculate metrics on key release
def on_release(key):
    global key_release_times, dwell_times, flight_times, up_down_times, backspace_count
    try:
        key_char = key.char
    except AttributeError:
        key_char = str(key)

    with buffer_lock:
        if key_char in key_press_times:
            press_time = key_press_times[key_char]
            release_time = time.time()
            dwell_time = release_time - press_time
            dwell_times.append(dwell_time)

            # Calculate Up-Down time
            if key_release_times:
                last_key = list(key_release_times.keys())[-1]
                up_down_time = press_time - key_release_times[last_key]
                up_down_times.append(up_down_time)

            # Calculate Down-Down time
            if len(key_release_times) > 0:
                last_release_time = list(key_release_times.values())[-1]
                flight_time = press_time - last_release_time
                flight_times.append(flight_time)

            # Update release time
            key_release_times[key_char] = release_time

        if key == keyboard.Key.backspace:
            backspace_count += 1

# Track mouse movements
def on_move(x, y):
    with buffer_lock:
        timestamp = time.time()
        if path_coordinates:
            last_x, last_y = path_coordinates[-1]
            distance = ((x - last_x)**2 + (y - last_y)**2)**0.5
            time_diff = timestamp - mouse_timestamps[-1] if mouse_timestamps else 0
            speed = distance / time_diff if time_diff > 0 else 0
            mouse_movements.append((distance, speed, timestamp))
        path_coordinates.append((x, y))
        mouse_timestamps.append(timestamp)

# Track mouse clicks
def on_click(x, y, button, pressed):
    action = 'pressed' if pressed else 'released'
    with buffer_lock:
        click_dynamics.append({'action': action, 'button': str(button), 'coordinates': (x, y), 'timestamp': time.time()})

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

# Start listeners for keyboard and mouse
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

