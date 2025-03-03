''' from django.urls import path

from .views import UserRegistrationView, LogoutView, UserLoginView
from . import views
from .views import log_web_action
from .models import KeystrokeLog, MouseLog

app_name = 'accounts'

urlpatterns = [
    path(
        "login/", UserLoginView.as_view(),
        name="user_login"
    ),
    path(
        "logout/", LogoutView.as_view(),
        name="user_logout"
    ),
    path(
        "register/", UserRegistrationView.as_view(),
        name="user_registration"
    ),
    path('save-keystroke-data/', views.save_keystroke_data, name='save_keystroke_data'),

    path('log-actions/', views.log_actions, name='log_actions'),
    path("log-web-action/", log_web_action, name="log_web_action"),
    path("log-keystroke/", log_keystroke, name="log_keystroke"),
    path("log-mouse/", log_mouse, name="log_mouse"),
]
''' 

from django.contrib import admin
from django.urls import path
from .views import UserRegistrationView, LogoutView, UserLoginView, log_web_action, save_keystroke_data, log_actions, log_keystroke, log_mouse

app_name = 'accounts'

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", LogoutView.as_view(), name="user_logout"),
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path('save-keystroke-data/', save_keystroke_data, name='save_keystroke_data'),
    path('log-actions/', log_actions, name='log_actions'),
    path("log-web-action/", log_web_action, name="log_web_action"),
    path("log-keystroke/", log_keystroke, name="log_keystroke"),
    path("log-mouse/", log_mouse, name="log_mouse"),
    path('admin/', admin.site.urls),
]
