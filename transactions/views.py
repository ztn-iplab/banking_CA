from dateutil.relativedelta import relativedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
# banking_system/app_name/views.py
import json
from django.http import JsonResponse
from .models import ActionLog
#import json
#from django.http import JsonResponse
from .models import WebActionLog
from .models import KeystrokeLog, MouseLog

from transactions.constants import DEPOSIT, WITHDRAWAL
from transactions.forms import (
    DepositForm,
    TransactionDateRangeForm,
    WithdrawForm,
)
from transactions.models import Transaction


class TransactionReportView(LoginRequiredMixin, ListView):
    """✅ Prevents errors for users without accounts"""
    
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    form_data = {}

    def get(self, request, *args, **kwargs):
        """✅ Redirect users without accounts before proceeding"""
        if not hasattr(self.request.user, 'account'):
            if self.request.user.is_superuser:
                return HttpResponseRedirect(reverse_lazy('admin'))  # ✅ Redirect admins
            return HttpResponseRedirect(reverse_lazy('accounts:no_account'))  # ✅ Redirect users without accounts

        form = TransactionDateRangeForm(request.GET or None)
        if form.is_valid():
            self.form_data = form.cleaned_data

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """✅ Only query transactions if the user has an account"""
        if not hasattr(self.request.user, 'account'):
            return Transaction.objects.none()  # ✅ Return empty queryset if user has no account

        queryset = super().get_queryset().filter(account=self.request.user.account)

        daterange = self.form_data.get("daterange")
        if daterange:
            queryset = queryset.filter(timestamp__date__range=daterange)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        """✅ Ensure 'account' is only accessed if it exists"""
        context = super().get_context_data(**kwargs)

        if hasattr(self.request.user, 'account'):
            context.update({
                'account': self.request.user.account,
                'form': TransactionDateRangeForm(self.request.GET or None)
            })
        else:
            context.update({'account': None})

        return context


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transactions:transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })

        return context

# Deposting money
class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit Money to Your Account'

    def get_initial(self):
        return {'transaction_type': DEPOSIT}

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account

        # ✅ Ensure the amount is valid
        if amount <= 0:
            messages.error(self.request, "Deposit amount must be greater than zero.")
            return self.form_invalid(form)

        # ✅ Update account balance
        if not account.initial_deposit_date:
            now = timezone.now()
            next_interest_month = int(12 / account.account_type.interest_calculation_per_year)
            account.initial_deposit_date = now
            account.interest_start_date = now + relativedelta(months=+next_interest_month)

        account.balance += amount
        account.save(update_fields=['initial_deposit_date', 'balance', 'interest_start_date'])

        messages.success(self.request, f'${amount:.2f} was deposited successfully! Your new balance is ${account.balance:.2f}')

        return self.render_to_response(self.get_context_data(form=form, account=account))



# WithDrawing Money
class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Money from Your Account'

    def get_initial(self):
        return {'transaction_type': WITHDRAWAL}

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account

        # ✅ Ensure the withdrawal amount is valid
        if amount <= 0:
            messages.error(self.request, "Invalid withdrawal amount. Please enter a valid amount.")
            return self.form_invalid(form)

        if account.balance < amount:
            messages.error(self.request, f"Insufficient funds! Your current balance is ${account.balance:.2f}")
            return self.form_invalid(form)

        # ✅ Deduct the amount and update balance
        account.balance -= amount
        account.save(update_fields=['balance'])

        messages.success(self.request, f'Withdrawal of ${amount:.2f} was successful! Your new balance is ${account.balance:.2f}')

        return self.render_to_response(self.get_context_data(form=form, account=account))


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
