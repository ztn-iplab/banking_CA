import os
import re

# Path to the settings.py file
SETTINGS_FILE = "banking_system/settings.py"  # Replace 'your_project' with your project folder name

# Path to urls.py files
URLS_FILE = "banking_system/urls.py"  # Replace 'your_app' with your app name

# Middleware to disable CSRF
MIDDLEWARE_CLASS = """
# Automatically added to disable CSRF checks
from django.utils.deprecation import MiddlewareMixin

class DisableCSRF(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
"""

# Middleware addition line
MIDDLEWARE_ADDITION = "'banking_system.middleware.DisableCSRF',"  # Replace 'your_project' with your middleware module

def disable_csrf_in_settings():
    print("[INFO] Modifying settings.py to disable CSRF...")

    with open(SETTINGS_FILE, "r") as file:
        settings = file.read()

    # Add DisableCSRF middleware
    if MIDDLEWARE_ADDITION not in settings:
        middleware_pattern = re.compile(r"MIDDLEWARE\s*=\s*\[[^\]]*\]", re.DOTALL)
        settings = middleware_pattern.sub(
            lambda m: m.group(0).replace("[", f"[\n    {MIDDLEWARE_ADDITION}"),
            settings
        )
        print("[INFO] Added DisableCSRF middleware to settings.py.")

    # Add DisableCSRF class
    if "class DisableCSRF" not in settings:
        settings += f"\n\n{MIDDLEWARE_CLASS}\n"
        print("[INFO] Added DisableCSRF class to settings.py.")

    with open(SETTINGS_FILE, "w") as file:
        file.write(settings)
    print("[SUCCESS] CSRF has been disabled in settings.py.")

def exempt_all_urls():
    print("[INFO] Modifying urls.py to exempt all views from CSRF...")

    with open(URLS_FILE, "r") as file:
        urls = file.read()

    csrf_exempt_import = "from django.views.decorators.csrf import csrf_exempt\n"
    csrf_exempt_pattern = "url_patterns = \[\n    csrf_exempt("

    # Add import and apply csrf_exempt
    if "csrf_exempt" not in urls:
        urls = urls.replace("from django.urls import ", f"{csrf_exempt_import}from django.urls import ")
        urls = urls.replace(
            "url_patterns = [",
            csrf_exempt_pattern
        )
        print("[INFO] Added csrf_exempt to all views in urls.py.")

    with open(URLS_FILE, "w") as file:
        file.write(urls)
    print("[SUCCESS] All views in urls.py are CSRF exempt.")

if __name__ == "__main__":
    print("[INFO] Starting CSRF disable script...")
    disable_csrf_in_settings()
    exempt_all_urls()
    print("[COMPLETE] CSRF exemptions applied. Restart your server to reflect changes.")

