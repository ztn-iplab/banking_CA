import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def update_views_file():
    """Automates adding CSRF handling to views."""
    views_path = os.path.join(BASE_DIR, "banking_system", "views.py")
    with open(views_path, "r") as file:
        content = file.read()

    # Check if `log_keystroke` and `log_mouse_action` exist
    if "def log_keystroke(request):" not in content:
        # Add the required views if not present
        additional_views = """
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def log_keystroke(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(f"Keystroke data received: {data}")
            return JsonResponse({"status": "success"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def log_mouse_action(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(f"Mouse data received: {data}")
            return JsonResponse({"status": "success"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)
"""
        content += additional_views

    with open(views_path, "w") as file:
        file.write(content)
    print("Updated views.py with necessary endpoints.")

def update_urls_file():
    """Automates URL registration for new views."""
    urls_path = os.path.join(BASE_DIR, "banking_system", "urls.py")
    with open(urls_path, "r") as file:
        content = file.read()

    # Add imports and paths if not already present
    if "log_keystroke" not in content:
        if "urlpatterns = [" in content:
            content = re.sub(r'urlpatterns = \[', """
urlpatterns = [
    path('log-keystroke/', views.log_keystroke, name='log_keystroke'),
    path('log-mouse-action/', views.log_mouse_action, name='log_mouse_action'),""", content)

        if "from . import views" not in content:
            content = "from . import views\n" + content

    with open(urls_path, "w") as file:
        file.write(content)
    print("Updated urls.py with necessary endpoints.")

def ensure_csrf_middleware():
    """Ensures CSRF middleware is active in settings."""
    settings_path = os.path.join(BASE_DIR, "banking_system", "settings.py")
    with open(settings_path, "r") as file:
        content = file.read()

    if "django.middleware.csrf.CsrfViewMiddleware" not in content:
        middleware_pattern = re.compile(r"MIDDLEWARE = \[(.*?)\]", re.DOTALL)
        content = middleware_pattern.sub(
            lambda m: f'MIDDLEWARE = [{m.group(1)}    \'django.middleware.csrf.CsrfViewMiddleware\',\n]', content
        )

    with open(settings_path, "w") as file:
        file.write(content)
    print("Ensured CSRF middleware in settings.")

def main():
    print("Automating setup...")
    update_views_file()
    update_urls_file()
    ensure_csrf_middleware()
    print("Setup automation completed!")

if __name__ == "__main__":
    main()

