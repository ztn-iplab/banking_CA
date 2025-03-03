from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import KeystrokeLog, MouseActionLog

admin.site.register(KeystrokeLog)
admin.site.register(MouseActionLog)
