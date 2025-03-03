''' from django.urls import path

from .views import DepositMoneyView, WithdrawMoneyView, TransactionRepostView

from . import views
from .views import log_web_action
from .models import KeystrokeLog, MouseLog

app_name = 'transactions'


urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("report/", TransactionRepostView.as_view(), name="transaction_report"),
    path("withdraw/", WithdrawMoneyView.as_view(), name="withdraw_money"),

    path('log-actions/', views.log_actions, name='log_actions'),
    path("log-web-action/", log_web_action, name="log_web_action"),

    path("log-keystroke/", log_keystroke, name="log_keystroke"),
    path("log-mouse/", log_mouse, name="log_mouse"),
]
''' 

from django.urls import path

from .views import DepositMoneyView, WithdrawMoneyView, TransactionRepostView, log_web_action, log_actions, log_keystroke, log_mouse

app_name = 'transactions'

urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("report/", TransactionRepostView.as_view(), name="transaction_report"),
    path("withdraw/", WithdrawMoneyView.as_view(), name="withdraw_money"),

    path('log-actions/', log_actions, name='log_actions'),
    path("log-web-action/", log_web_action, name="log_web_action"),

    path("log-keystroke/", log_keystroke, name="log_keystroke"),
    path("log-mouse/", log_mouse, name="log_mouse"),
]

