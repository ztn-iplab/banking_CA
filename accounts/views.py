from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect, redirect,render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegistrationForm, UserAddressForm
from .models import KeystrokeData

# banking_system/app_name/views.py
import json
from django.http import JsonResponse
from .models import ActionLog

#import json
#from django.http import JsonResponse
from .models import WebActionLog
from .models import KeystrokeLog, MouseLog

User = get_user_model()


@csrf_exempt
def save_keystroke_data(request):
    if request.method == 'POST':
        # Extract data from the POST request
        keystrokes_data = request.POST.get('inputPhrase', '')  # Match the field name in the HTML form
        
        # Save the keystroke data to the database
        KeystrokeData.objects.create(data=keystrokes_data)
        
        # Return a JSON response indicating success
        return JsonResponse({'status': 'success'})
    else:
        # Return a JSON response indicating failure (only accept POST requests)
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)



class UserRegistrationView(TemplateView):
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        """✅ Redirect authenticated users appropriately"""
        if request.user.is_authenticated:
            user = request.user

            if user.is_superuser:
                return HttpResponseRedirect('/admin/')

            if hasattr(user, 'account'):
                return HttpResponseRedirect('/transactions/report/')

            return HttpResponseRedirect('/accounts/no-account/')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """✅ Load blank forms by default or preserve them with errors"""
        context = super().get_context_data(**kwargs)
        context['registration_form'] = kwargs.get('registration_form') or UserRegistrationForm()
        context['address_form'] = kwargs.get('address_form') or UserAddressForm()
        return context

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(request.POST)
        address_form = UserAddressForm(request.POST)

        if registration_form.is_valid() and address_form.is_valid():
            user = registration_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()

            messages.success(request, "Registration successful! You can now log in.")
            return redirect("login")

        messages.error(request, "Please correct the errors below.")
        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                address_form=address_form
            )
        )


class UserLoginView(LoginView):
    """✅ Prevent admins and users without accounts from going to /transactions/report/"""
    
    template_name = 'accounts/user_login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        """✅ After login, check user role and redirect accordingly"""
        user = form.get_user()
        login(self.request, user)

        if user.is_superuser:  # ✅ Redirect admin to admin dashboard
            return redirect('/admin/')
        
        if hasattr(user, 'account'):  # ✅ Ensure the user has an account before redirecting
            return redirect('/transactions/report/')
        else:
            return redirect('/accounts/no-account/')  # ✅ Redirect users without an account



# Users without accounts
def no_account_view(request):
    """✅ Show a message when a user has no account"""
    return render(request, 'accounts/no_account.html', {"message": "You do not have an account linked to your user."})

# Logout View
class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)




def log_actions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Save keystrokes, mouse movements, and actions to the database
        for entry in data['keystrokes']:
            ActionLog.objects.create(action_type='keystroke', details=entry)

        for entry in data['mouseMoves']:
            ActionLog.objects.create(action_type='mouse_move', details=entry)

        for entry in data['siteActions']:
            ActionLog.objects.create(action_type='site_action', details=entry)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)



def log_web_action(request):
    if request.method == "POST":
        data = json.loads(request.body)
        WebActionLog.objects.create(
            user=data.get("user"),
            action=data.get("action"),
            element=data.get("element")
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)

#from .models import KeystrokeLog, MouseLog

def log_keystroke(request):
    if request.method == "POST":
        data = json.loads(request.body)
        KeystrokeLog.objects.create(
            user=data.get("user"),
            key=data.get("key"),
            timestamp=data.get("timestamp"),
            duration=data.get("duration", 0)
        )
        return JsonResponse({"status": "success"})

def log_mouse(request):
    if request.method == "POST":
        data = json.loads(request.body)
        MouseLog.objects.create(
            user=data.get("user"),
            x_position=data.get("x_position"),
            y_position=data.get("y_position"),
            timestamp=data.get("timestamp")
        )
        return JsonResponse({"status": "success"})

