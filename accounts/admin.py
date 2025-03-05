from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.urls import reverse
from .models import KeystrokeLog, MouseLog, WebActionLog, BankAccountType, User, UserAddress, UserBankAccount

# ✅ Custom Django Admin Site (Fixes Jet Dashboard Logout)
class CustomAdminSite(AdminSite):
    """Custom Django Admin with Correct Logout Link."""
    site_header = "IPLab Banking Admin"
    site_title = "Admin Portal"
    index_title = "Welcome to IPLab Banking Admin"

    def each_context(self, request):
        """✅ Override each_context to set the correct logout URL"""
        context = super().each_context(request)
        context["logout_url"] = reverse("admin_logout")  # ✅ This fixes the NoReverseMatch error
        return context

# ✅ Create a Custom Admin Site
admin_site = CustomAdminSite(name="custom_admin")


# ✅ Ensure all models are registered properly under `admin_site`
admin_site.register(BankAccountType)
admin_site.register(User)
admin_site.register(UserAddress)
admin_site.register(UserBankAccount)
admin_site.register(KeystrokeLog)
admin_site.register(MouseLog)
admin_site.register(WebActionLog)

# ✅ Register the custom admin site globally
admin.site = admin_site
