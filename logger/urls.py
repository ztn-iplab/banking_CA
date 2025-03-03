from django.urls import path
from . import views

urlpatterns = [
    path('api/log-mouse-action/', views.log_mouse_action, name='log_mouse_action'),
    path('api/log-keystroke/', views.log_keystroke, name='log_keystroke'),
]
