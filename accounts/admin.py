from django.contrib import admin
from .models import KeystrokeLog, MouseLog, WebActionLog
from .models import BankAccountType, User, UserAddress, UserBankAccount


admin.site.register(BankAccountType)
admin.site.register(User)
admin.site.register(UserAddress)
admin.site.register(UserBankAccount)

# In accounts/admin.py
#from django.contrib import admin
#from .models import KeystrokeLog, MouseLog, WebActionLog

admin.site.register(KeystrokeLog)
admin.site.register(MouseLog)
admin.site.register(WebActionLog)
