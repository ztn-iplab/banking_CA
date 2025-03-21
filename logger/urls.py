from django.urls import path
from . import views

# urlpatterns = [
#     path('api/log-mouse-action/', views.log_mouse_action, name='log_mouse_action'),
#     path('api/log-keystroke/', views.log_keystroke, name='log_keystroke'),
# ]

from logger.views import log_biometrics

urlpatterns = [
    path("api/biometrics/log", log_biometrics, name="log_biometrics"),
]
