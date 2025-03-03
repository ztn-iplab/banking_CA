from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

# Model for keystroke logging
class KeystrokeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    key = models.CharField(max_length=255)  # Stores the key pressed or released
    action = models.CharField(max_length=10, choices=[('press', 'Press'), ('release', 'Release')])  # Whether it was a press or release
    rhythm = models.FloatField(null=True, blank=True)  # Typing rhythm (time between key actions in seconds)
    dwell_time = models.FloatField(null=True, blank=True)  # Time the key was held down (dwell time)
    flight_time = models.FloatField(null=True, blank=True)  # Time between key presses (flight time)
    up_down_time = models.FloatField(null=True, blank=True)  # Time between release and press of other keys (up-down time)
    session_duration = models.FloatField(null=True, blank=True)  # Session duration for keystrokes
    timestamp = models.DateTimeField(auto_now_add=True)  # Time when the action occurred

    def __str__(self):
        return f"{self.action.capitalize()} Key: {self.key}, Rhythm: {self.rhythm}, Dwell Time: {self.dwell_time}, Flight Time: {self.flight_time}, Up-Down Time: {self.up_down_time}, at {self.timestamp}"

# Model for mouse action logging
class MouseActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=50, choices=[('move', 'Move'), ('click', 'Click'), ('scroll', 'Scroll')])  # Type of action
    coordinates = models.CharField(max_length=50)  # Mouse position as (x, y)
    button = models.CharField(max_length=10, choices=[('left', 'Left'), ('right', 'Right'), ('middle', 'Middle')], null=True, blank=True)  # Mouse button used
    delta = models.CharField(max_length=50, null=True, blank=True)  # Scroll delta (for scroll actions)
    timestamp = models.DateTimeField(auto_now_add=True)  # Time when the action occurred
    distance = models.FloatField(null=True, blank=True)  # Distance moved (for move actions)
    speed = models.FloatField(null=True, blank=True)  # Speed of the movement (for move actions)

    def __str__(self):
        details = f"Action: {self.action.capitalize()}, Coordinates: {self.coordinates}, at {self.timestamp}"
        if self.button:
            details += f", Button: {self.button.capitalize()}"
        if self.delta:
            details += f", Delta: {self.delta}"
        if self.distance:
            details += f", Distance: {self.distance} px"
        if self.speed:
            details += f", Speed: {self.speed} px/sec"
        return details

# Model for backspace count logging
class BackspaceCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    count = models.IntegerField(default=0)  # Stores the number of backspaces pressed
    timestamp = models.DateTimeField(auto_now_add=True)  # Time when the count was logged

    def __str__(self):
        return f"Backspace Count: {self.count} at {self.timestamp}"

class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.last_activity}"

