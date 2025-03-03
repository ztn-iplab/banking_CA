from django.db import models

# Create your models here.
# banking_system/app_name/models.py

class ActionLog(models.Model):
    action_type = models.CharField(max_length=20)
    details = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} - {self.timestamp}"

class KeystrokeLog(models.Model):
    user = models.CharField(max_length=50)
    key = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField()  # Capture key hold time

    def __str__(self):
        return f"{self.user}: {self.key} at {self.timestamp}"

class MouseLog(models.Model):
    user = models.CharField(max_length=50)
    x_position = models.FloatField()
    y_position = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mouse at ({self.x_position}, {self.y_position})"

class WebActionLog(models.Model):
    user = models.CharField(max_length=50)
    action = models.CharField(max_length=50)  # e.g., click, scroll
    element = models.CharField(max_length=100)  # e.g., button, link
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} on {self.element} by {self.user}"

