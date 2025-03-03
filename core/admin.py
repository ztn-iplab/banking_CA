from django.contrib import admin

# Register your models here.
# In accounts/admin.py
#from django.contrib import admin
from .models import KeystrokeLog, MouseLog, WebActionLog

admin.site.register(KeystrokeLog)
admin.site.register(MouseLog)
admin.site.register(WebActionLog)
