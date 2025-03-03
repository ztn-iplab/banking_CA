# analytics/routing.py

from django.urls import path
from .consumers import KeystrokeDataConsumer

websocket_urlpatterns = [
    path('ws/save-keystroke-data/', KeystrokeDataConsumer.as_asgi()),
]
