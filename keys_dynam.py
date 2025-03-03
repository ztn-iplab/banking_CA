import os
import sys
import django
import time
import threading
from pynput import keyboard, mouse
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add the parent directory of 'banking_system' to sys.path
sys.path.append('/home/mutabazi/Documents/Projects/banking_system')

# Set the environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')

# Initialize Django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.sessions.models import Session
from logger.models import KeystrokeLog, MouseActionLog, BackspaceCount, UserActivity

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

# Track user activity
last_activity_time = time.time()
INACTIVITY_THRESHOLD = 300  # 5 minutes
USER_LOGGED_OUT = False  # Track logout status

from django.utils import timezone

def get_current_user():
    try:
        # Check for the active session without requiring a request object
        session = Session.objects.filter(expire_date__gte=timezone.now()).last()
        
        if session:
            session_data = session.get_decoded()  # Decode the session data
            user_id = session_data.get('_auth_user_id')
            
            if user_id:
                user = User.objects.get(id=user_id)
                if user and user.is_active and not user.is_superuser:
                    logger.debug(f"Active session found: User ID {user.id} - Email: {user.email}")
                    return user
                else:
                    logger.debug(f"Session found, but user is either not valid, inactive, or a superuser.")
            else:
                logger.debug("User ID not found in session data.")
        else:
            logger.debug("No active session found.")
            
    except Exception as e:
        logger.error(f"Error fetching user from session: {e}")
    
    return None

# def get_current_user(request):
#     try:
#         # Ensure that the user is interacting with the system via URL
#         if not request.user.is_authenticated or request.user.is_superuser:
#             logger.debug("No active user or superuser is logged in.")
#             return None
        
#         # Fetch the most recent session that is active
#         session = Session.objects.filter(expire_date__gte=timezone.now()).last()
        
#         if session:
#             session_data = session.get_decoded()  # Decode the session data
#             user_id = session_data.get('_auth_user_id')
            
#             if user_id:
#                 # Fetch the user object based on the ID
#                 user = User.objects.get(id=user_id)
                
#                 if user and user.is_active and not user.is_superuser:
#                     logger.debug(f"Active session found: User ID {user.id} - Email: {user.email}")
#                     return user
#                 else:
#                     logger.debug(f"Session found, but user is either not valid, inactive, or a superuser.")
#             else:
#                 logger.debug("User ID not found in session data.")
#         else:
#             logger.debug("No active session found.")
            
#     except Exception as e:
#         logger.error(f"Error fetching user from session: {e}")
    
#     return None

def record_user_activity():
    global last_activity_time
    last_activity_time = time.time()
    user = get_current_user()
    if user:
        UserActivity.objects.create(user=user, last_activity=last_activity_time)
        logger.debug(f"Recorded activity for user: {user.username}")
    else:
        logger.debug("No active user to record activity.")
        

def logout_user():
    global USER_LOGGED_OUT
    user = get_current_user()
    if user and not USER_LOGGED_OUT:
        # End user session by logging out
        session = Session.objects.filter(session_key=user.session_key).first()
        if session:
            session.delete()  # Delete the session to log the user out
            logger.debug(f"User {user.username} logged out due to inactivity.")
            USER_LOGGED_OUT = True
        else:
            logger.debug(f"No active session for {user.username} to log out.")
    else:
        logger.debug("User already logged out or no session to end.")

def on_press(key):
    try:
        key_char = key.char or str(key)
    except AttributeError:
        key_char = str(key)
    with buffer_lock:
        key_press_times[key_char] = time.time()
        record_user_activity()

def on_release(key):
    try:
        key_char = key.char or str(key)
    except AttributeError:
        key_char = str(key)
    
    with buffer_lock:
        if key_char in key_press_times:
            press_time = key_press_times[key_char]
            release_time = time.time()

            # Debugging for rhythm calculation
            logger.debug(f"Key: {key_char} - Press Time: {press_time} - Release Time: {release_time}")
            
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
        record_user_activity()

def on_click(x, y, button, pressed):
    with buffer_lock:
        action = 'pressed' if pressed else 'released'
        click_dynamics.append({
            'action': action,
            'button': str(button),
            'coordinates': (x, y),
            'timestamp': time.time()
        })
        record_user_activity()

def check_inactivity():
    while True:
        if time.time() - last_activity_time > INACTIVITY_THRESHOLD:
            logout_user()  # Log out the user after inactivity
            break
        time.sleep(60)

def display_metrics():
    logger.debug("\nKeystroke Dynamics Metrics:")
    logger.debug(f"Average Dwell Time: {sum(dwell_times) / len(dwell_times) if dwell_times else 0:.4f} seconds")
    logger.debug(f"Average Flight Time: {sum(flight_times) / len(flight_times) if flight_times else 0:.4f} seconds")
    logger.debug(f"Average Up-Down Time: {sum(up_down_times) / len(up_down_times) if up_down_times else 0:.4f} seconds")
    logger.debug(f"Backspace Count: {backspace_count}")

    logger.debug("\nMouse Dynamics Metrics:")
    if mouse_movements:
        total_distance = sum([m[0] for m in mouse_movements])
        total_speed = sum([m[1] for m in mouse_movements])
        logger.debug(f"Total Movement Distance: {total_distance:.2f} pixels")
        logger.debug(f"Average Speed: {total_speed / len(mouse_movements):.2f} pixels per second")
    logger.debug(f"Click Dynamics: {len(click_dynamics)} clicks logged")
    logger.debug(f"Pointer Path Points: {len(path_coordinates)} points logged")

    log_data()

def log_data():
    try:
        user = get_current_user()
        if user:
            session_start = time.time()  # Capture session start
            # Iterate over a copy of the key_release_times dictionary to avoid modifying it while iterating
            for key_char, release_time in key_release_times.copy().items():
                dwell_time = dwell_times.pop(0) if dwell_times else 0
                flight_time = flight_times.pop(0) if flight_times else 0
                up_down_time = up_down_times.pop(0) if up_down_times else 0
                
                session_end = time.time()
                session_duration = session_end - session_start  # Calculate session duration

                KeystrokeLog.objects.create(
                    user=user,
                    key=key_char,
                    action="release",
                    rhythm=release_time - key_press_times[key_char],
                    dwell_time=dwell_time,
                    flight_time=flight_time,
                    up_down_time=up_down_time,
                    session_duration=session_duration  # Log session duration here
                )

            for click in click_dynamics:
                MouseActionLog.objects.create(
                    user=user,
                    action=click['action'],
                    coordinates=str(click['coordinates']),
                    button=click['button'],
                    distance=0,
                    speed=0,
                    timestamp=click['timestamp']
                )

            BackspaceCount.objects.create(user=user, count=backspace_count)
            logger.debug("Data logged successfully.")
        else:
            logger.error("No user logged in.")
    except Exception as e:
        logger.error(f"Failed to log data: {e}")


def start_listeners():
    logger.debug("Starting keyboard and mouse listeners...")
    threading.Thread(target=check_inactivity, daemon=True).start()
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
    
    logger.debug("Starting the listeners...")
    keyboard_listener.start()
    mouse_listener.start()
    keyboard_listener.join()
    mouse_listener.join()

if __name__ == "__main__":
    logger.info("Keystroke and Mouse Dynamics Logger is running. Press Ctrl+C to stop and display metrics.")
    try:
        start_listeners()
    except KeyboardInterrupt:
        display_metrics()
        logger.info("Program terminated by user.")

