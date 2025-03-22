from django.urls import path
from . import views

from logger.views import log_biometrics

urlpatterns = [
    path("api/biometrics/log", log_biometrics, name="log_biometrics"),
]
