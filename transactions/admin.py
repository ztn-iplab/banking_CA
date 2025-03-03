from django.contrib import admin
from .models import KeystrokeLog, MouseLog, WebActionLog
from transactions.models import Transaction

admin.site.register(Transaction)

# In transactions/admin.py
#from django.contrib import admin
#from .models import KeystrokeLog, MouseLog, WebActionLog

admin.site.register(KeystrokeLog)
admin.site.register(MouseLog)
admin.site.register(WebActionLog)
