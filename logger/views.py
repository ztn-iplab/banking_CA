
import json
from django.http import JsonResponse
from .models import KeystrokeLog

def log_keystroke(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data
            keystrokes = data.get('data')  # Access the "data" key

            # Save each keystroke in the database
            for keystroke in keystrokes:
                key = keystroke.get('key')
                if key:  # Save only if 'key' is present
                    KeystrokeLog.objects.create(key=key)

            print(f"Keystrokes received: {keystrokes}")

            return JsonResponse({"status": "success", "message": "Keystrokes logged successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

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
