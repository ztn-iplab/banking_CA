import os

def ensure_function_in_file(file_path, function_code, function_name):
    """Ensure a specific function exists in a file."""
    with open(file_path, 'r') as f:
        content = f.read()

    if function_name not in content:
        with open(file_path, 'a') as f:  # Append instead of overwriting
            f.write(f"\n{function_code}\n")
        print(f"Added '{function_name}' to {file_path}")
    else:
        print(f"'{function_name}' already exists in {file_path}")

def update_django_views():
    """Ensure both log_keystroke and log_mouse_action are present."""
    backend_view_path = '/home/mutabazi/Documents/Users/festusedward-n/Backup for the project/26th November 2024 Backup/banking_system/logger/views.py'

    log_keystroke_code = """
def log_keystroke(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            keystrokes = data.get('data')
            print(f"Keystrokes received: {keystrokes}")
            return JsonResponse({"status": "success", "message": "Keystrokes logged successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
    """

    log_mouse_action_code = """
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
    """

    ensure_function_in_file(backend_view_path, log_keystroke_code, 'log_keystroke')
    ensure_function_in_file(backend_view_path, log_mouse_action_code, 'log_mouse_action')


if __name__ == "__main__":
    print("Starting updates...")
    update_django_views()

