import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from dateutil import parser

from .models import KeystrokeLog, MouseActionLog

@csrf_exempt
def log_biometrics(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

    try:
        # Check user auth (optional if you're not using @login_required)
        if not request.user.is_authenticated:
            return JsonResponse({"status": "unauthorized"}, status=401)

        data = json.loads(request.body)
        keystrokes = data.get("keystrokes", [])
        mouse_actions = data.get("mouse", [])

        for k in data.get("keystrokes", []):
            KeystrokeLog.objects.create(
            user=request.user,
            key=k["key"],
            action=k.get("event", "press"),
            dwell_time=k.get("dwell_time", 0),
            flight_time=k.get("flight_time", 0),
            up_down_time=k.get("up_down_time", 0),
            rhythm=k.get("rhythm", 0),
            session_duration=k.get("session_duration", 0),
            timestamp=parser.isoparse(k.get("timestamp"))
    )

        for m in data.get("mouse", []):
            MouseActionLog.objects.create(
                user=request.user,
                action=m["action"],
                coordinates=m["coordinates"],
                button=m.get("button", ""),
                delta=m.get("delta", ""),
                distance=m.get("distance", 0),
                speed=m.get("speed", 0),
                timestamp=parser.isoparse(m.get("timestamp"))
            )
        print(f"Logged {len(data.get('keystrokes', []))} keystrokes and {len(data.get('mouse', []))} mouse movements.")
        print("📥 MouseAction Received:", m)
        print("📍 Button value:", m.get("button"))
        print("📥 Incoming button value:", m.get("button"))  # debug

        return JsonResponse({"status": "success", "message": "Biometrics logged successfully"}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
