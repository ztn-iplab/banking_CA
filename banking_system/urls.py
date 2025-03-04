from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.urls import include, path
from accounts.admin import admin_site  # ✅ Custom Admin
from core.views import HomeView, admin_logout
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

    # Logging & Monitoring
    path('log-actions/', views.log_actions, name='log_actions'),
    path("log-web-action/", log_web_action, name="log_web_action"),
    path("log-keystroke/", log_keystroke, name="log_keystroke"),
    path("log-mouse/", views.log_mouse, name="log_mouse"),

    # Include transaction URLs
    path('transactions/', include('transactions.urls', namespace='transactions')),

    # Include logger app URLs
    path('', include('logger.urls')),

    # ✅ Admin Logout Route (Only One Logout)
    path("admin/logout/", admin_logout, name="admin_logout"),
    
    # ✅ Use Custom Admin Site (NO DUPLICATES)
    path("admin/", admin_site.urls),  # ✅ Only this should handle /admin/
]
