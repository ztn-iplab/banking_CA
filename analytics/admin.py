from django.contrib import admin
from .models import KeystrokeLog, MouseLog, WebActionLog
# Register your models here.
# analytics/admin.py


from .models import KeystrokeData

@admin.register(KeystrokeData)
class KeystrokeDataAdmin(admin.ModelAdmin):
    list_display = ['key', 'timestamp']

# In analytics/admin.py
#from django.contrib import admin
#from .models import KeystrokeLog, MouseLog, WebActionLog

admin.site.register(KeystrokeLog)
admin.site.register(MouseLog)
admin.site.register(WebActionLog)
