from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
# banking_system/app_name/views.py
import json
from django.http import JsonResponse
from .models import ActionLog
#import json
#from django.http import JsonResponse
from .models import WebActionLog
from .models import KeystrokeLog, MouseLog

class HomeView(TemplateView):
    template_name = 'core/index.html'




def log_actions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Save keystrokes, mouse movements, and actions to the database
        for entry in data['keystrokes']:
            ActionLog.objects.create(action_type='keystroke', details=entry)

        for entry in data['mouseMoves']:
            ActionLog.objects.create(action_type='mouse_move', details=entry)

        for entry in data['siteActions']:
            ActionLog.objects.create(action_type='site_action', details=entry)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)



def log_web_action(request):
    if request.method == "POST":
        data = json.loads(request.body)
        WebActionLog.objects.create(
            user=data.get("user"),
            action=data.get("action"),
            element=data.get("element")
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)

#from .models import KeystrokeLog, MouseLog

def log_keystroke(request):
    if request.method == "POST":
        data = json.loads(request.body)
        KeystrokeLog.objects.create(
            user=data.get("user"),
            key=data.get("key"),
            timestamp=data.get("timestamp"),
            duration=data.get("duration", 0)
        )
        return JsonResponse({"status": "success"})

def log_mouse(request):
    if request.method == "POST":
        data = json.loads(request.body)
        MouseLog.objects.create(
            user=data.get("user"),
            x_position=data.get("x_position"),
            y_position=data.get("y_position"),
            timestamp=data.get("timestamp")
        )
        return JsonResponse({"status": "success"})


#For logging out:

@csrf_exempt  # ✅ Disable CSRF for Logout
def admin_logout(request):
    """✅ Allow Logout via GET and POST, then Redirect"""
    if request.method in ["POST", "GET"]:  # ✅ Accept both GET and POST
        logout(request)
        request.session.flush()  # ✅ Clears session data

        # ✅ Redirect to the login page
        return HttpResponseRedirect(reverse("admin:login"))  # ✅ Redirect Admin to Login Page

    return JsonResponse({"error": "Invalid request"}, status=400)