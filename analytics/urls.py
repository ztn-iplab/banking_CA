# analytics/urls.py

from django.urls import path
from . import views
from .views import log_web_action
from .models import KeystrokeLog, MouseLog

app_name = 'analytics'  # Define app-level namespace

urlpatterns = [
    # Define the URL pattern for submitting keystroke data
    path('/save-keystroke-data/', views.save_keystroke_data, name='save_keystroke_data'),
    path('log-actions/', views.log_actions, name='log_actions'),
    path("log-web-action/", log_web_action, name="log_web_action"),
    path("log-keystroke/", log_keystroke, name="log_keystroke"),
    path("log-mouse/", log_mouse, name="log_mouse"),
]

