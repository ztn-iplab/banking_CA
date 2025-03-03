"""banking_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.views.decorators.csrf import csrf_exempt
from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.urls import include, path

from core.views import HomeView
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from . import views
from .views import log_web_action
from .models import KeystrokeLog, MouseLog

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('accounts/', include('django.contrib.auth.urls')),  # Include authentication URLs
    path('admin/', admin.site.urls),
    path('log-actions/', views.log_actions, name='log_actions'),
    path("log-web-action/", log_web_action, name="log_web_action"),
    path("log-keystroke/", log_keystroke, name="log_keystroke"),
    path("log-mouse/", log_mouse, name="log_mouse"),
    path(
        'transactions/',
        include('transactions.urls', namespace='transactions')
    )
    
]
"""

from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.urls import include, path

from core.views import HomeView
from . import views
from .views import log_web_action, log_keystroke  # Added log_keystroke import

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    
    # Fix: Merge authentication URLs properly
    path('accounts/', include([
        path('', include('accounts.urls', namespace='accounts')),
        path('', include('django.contrib.auth.urls')),
        
    ])),

    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),

    # Logging & Monitoring
    path('log-actions/', views.log_actions, name='log_actions'),
    path("log-web-action/", log_web_action, name="log_web_action"),
    path("log-keystroke/", log_keystroke, name="log_keystroke"),
    path("log-mouse/", views.log_mouse, name="log_mouse"),

    # Include transaction URLs
    path('transactions/', include('transactions.urls', namespace='transactions')),

    # Include logger app URLs
    path('', include('logger.urls')),
]



