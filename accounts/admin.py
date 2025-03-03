from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin.sites import AdminSite
from .models import KeystrokeLog, MouseLog, WebActionLog
from .models import BankAccountType, User, UserAddress, UserBankAccount

# Set Django Admin Titles
admin.site.site_header = "IPLab Banking Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to IPLab Banking Admin"

# Ensure CSS is included in Django Admin
class CustomAdminSite(AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context["custom_css"] = "admin/css/admin_custom.css"  # Make sure this exists
        return context

admin.site = CustomAdminSite()

# Register models
admin.site.register(BankAccountType)
admin.site.register(User)
admin.site.register(UserAddress)
admin.site.register(UserBankAccount)
admin.site.register(KeystrokeLog)
admin.site.register(MouseLog)
admin.site.register(WebActionLog)
