from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
# analytics/models.py


class KeystrokeData(models.Model):
    key = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

# banking_system/app_name/models.py
#from django.db import models

class ActionLog(models.Model):
    action_type = models.CharField(max_length=20)
    details = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} - {self.timestamp}"



#from django.db import models

#class WebActionLog(models.Model):
    #action_type = models.CharField(max_length=20)  # Type of action (e.g., login, logout, transaction)
    #details = models.JSONField()  # Additional details about the action
    #user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who performed the action
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analytics_web_action_logs')
    #timestamp = models.DateTimeField(auto_now_add=True)  # Time when the action was logged
class WebActionLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analytics_web_action_logs')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.action_type} by {self.user} at {self.timestamp}"

#from django.db import models

class KeystrokeLog(models.Model):
    user = models.CharField(max_length=100)  # Username or user identifier
    key = models.CharField(max_length=10)  # Key pressed
    event_type = models.CharField(max_length=10, choices=[('down', 'KeyDown'), ('up', 'KeyUp')])
    timestamp = models.DateTimeField()  # Time of the event

    class Meta:
        verbose_name = "Keystroke Log"
        verbose_name_plural = "Keystroke Logs"

    def __str__(self):
        return f"{self.user} - {self.key} ({self.event_type}) at {self.timestamp}"

class MouseLog(models.Model):
    user = models.CharField(max_length=100)  # Username or user identifier
    action = models.CharField(max_length=50, choices=[('move', 'Move'), ('click', 'Click'), ('scroll', 'Scroll')])
    x_coordinate = models.FloatField()  # X-axis coordinate of the mouse
    y_coordinate = models.FloatField()  # Y-axis coordinate of the mouse
    timestamp = models.DateTimeField()  # Time of the event

    class Meta:
        verbose_name = "Mouse Log"
        verbose_name_plural = "Mouse Logs"

    def __str__(self):
        return f"{self.user} - {self.action} at ({self.x_coordinate}, {self.y_coordinate}) on {self.timestamp}"
