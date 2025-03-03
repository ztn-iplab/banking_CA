import os

# Paths to relevant files
views_path = "/home/mutabazi/Documents/Users/festusedward-n/Backup for the project/26th November 2024 Backup/banking_system/logger/views.py"
urls_path = "/home/mutabazi/Documents/Users/festusedward-n/Backup for the project/26th November 2024 Backup/banking_system/logger/urls.py"

# Correct implementation of log_mouse_action
log_mouse_action_code = """
def log_mouse_action(request):
    from django.http import JsonResponse
    import json
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            action = data.get("action")
            coordinates = data.get("coordinates")
            # Log or process the data
            print(f"Mouse action: {action}, Coordinates: {coordinates}")
            return JsonResponse({"status": "success", "message": "Mouse action logged successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
"""

# Correct implementation of log_keystroke
log_keystroke_code = """
def log_keystroke(request):
    from django.http import JsonResponse
    import json
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            keystrokes = data.get("data")
            # Log or process the keystrokes
            print(f"Keystrokes: {keystrokes}")
            return JsonResponse({"status": "success", "message": "Keystrokes logged successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
"""

# Function to update views.py
def update_views():
    print(f"Checking {views_path}...")
    if not os.path.exists(views_path):
        print(f"Error: {views_path} not found.")
        return

    with open(views_path, 'r+') as f:
        content = f.read()
        updated = False

        if "def log_mouse_action" not in content:
            print("Adding log_mouse_action function...")
            f.write("\n" + log_mouse_action_code.strip() + "\n")
            updated = True

        if "def log_keystroke" not in content:
            print("Adding log_keystroke function...")
            f.write("\n" + log_keystroke_code.strip() + "\n")
            updated = True

        if not updated:
            print("No changes needed for views.py.")
        else:
            print("views.py updated successfully.")

# Correct URL patterns
correct_urls_code = """
from django.urls import path
from . import views

urlpatterns = [
    path('api/log-mouse-action/', views.log_mouse_action, name='log_mouse_action'),
    path('api/log-keystroke/', views.log_keystroke, name='log_keystroke'),
]
"""

# Function to update urls.py
def update_urls():
    print(f"Checking {urls_path}...")
    if not os.path.exists(urls_path):
        print(f"Error: {urls_path} not found.")
        return

    with open(urls_path, 'w') as f:
        print("Updating urls.py with correct URL patterns...")
        f.write(correct_urls_code.strip())
        print("urls.py updated successfully.")

# Run the fixes
if __name__ == "__main__":
    print("Starting automatic fixes...")
    update_views()
    update_urls()
    print("All fixes applied successfully.")

