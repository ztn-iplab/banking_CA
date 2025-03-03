from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models

from .constants import GENDER_CHOICE
from .managers import UserManager



from django.db import models
from django.conf import settings 
# Create your models here.
# analytics/models.py


class KeystrokeData(models.Model):
    key = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)



class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def balance(self):
        if hasattr(self, 'account'):
            return self.account.balance
        return 0


class BankAccountType(models.Model):
    name = models.CharField(max_length=128)
    maximum_withdrawal_amount = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    annual_interest_rate = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        decimal_places=2,
        max_digits=5,
        help_text='Interest rate from 0 - 100'
    )
    interest_calculation_per_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text='The number of times interest will be calculated per year'
    )

    def __str__(self):
        return self.name

    def calculate_interest(self, principal):
        """
        Calculate interest for each account type.

        This uses a basic interest calculation formula
        """
        p = principal
        r = self.annual_interest_rate
        n = Decimal(self.interest_calculation_per_year)

        # Basic Future Value formula to calculate interest
        interest = (p * (1 + ((r/100) / n))) - p

        return round(interest, 2)


class UserBankAccount(models.Model):
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE,
    )
    account_type = models.ForeignKey(
        BankAccountType,
        related_name='accounts',
        on_delete=models.CASCADE
    )
    account_no = models.PositiveIntegerField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    birth_date = models.DateField(null=True, blank=True)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    interest_start_date = models.DateField(
        null=True, blank=True,
        help_text=(
            'The month number that interest calculation will start from'
        )
    )
    initial_deposit_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.account_no)

    def get_interest_calculation_months(self):
        """
        List of month numbers for which the interest will be calculated

        returns [2, 4, 6, 8, 10, 12] for every 2 months interval
        """
        interval = int(
            12 / self.account_type.interest_calculation_per_year
        )
        start = self.interest_start_date.month
        return [i for i in range(start, 13, interval)]


class UserAddress(models.Model):
    user = models.OneToOneField(
        User,
        related_name='address',
        on_delete=models.CASCADE,
    )
    street_address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    postal_code = models.PositiveIntegerField()
    country = models.CharField(max_length=256)

    def __str__(self):
        return self.user.email


# banking_system/app_name/models.py

class ActionLog(models.Model):
    action_type = models.CharField(max_length=20)
    details = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} - {self.timestamp}"



#from django.db import models

class WebActionLog(models.Model):
    action_type = models.CharField(max_length=20)  # Type of action (e.g., login, logout, transaction)
    details = models.JSONField()  # Additional details about the action
    #user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who performed the action
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts_webactionlogs')
    timestamp = models.DateTimeField(auto_now_add=True)  # Time when the action was logged

    def __str__(self):
        return f"{self.action_type} by {self.user} at {self.timestamp}"

#from django.db import models

class KeystrokeLog(models.Model):
    user = models.CharField(max_length=100)  # Username or user identifier
    key = models.CharField(max_length=10)  # Key pressed
    event_type = models.CharField(max_length=10, choices=[('down', 'KeyDown'), ('up', 'KeyUp')])
    timestamp = models.DateTimeField()  # Time of the event

    class Meta:
        verbose_name = "Keystroke Log"
        verbose_name_plural = "Keystroke Logs"

    def __str__(self):
        return f"{self.user} - {self.key} ({self.event_type}) at {self.timestamp}"

class MouseLog(models.Model):
    user = models.CharField(max_length=100)  # Username or user identifier
    action = models.CharField(max_length=50, choices=[('move', 'Move'), ('click', 'Click'), ('scroll', 'Scroll')])
    x_coordinate = models.FloatField()  # X-axis coordinate of the mouse
    y_coordinate = models.FloatField()  # Y-axis coordinate of the mouse
    timestamp = models.DateTimeField()  # Time of the event

    class Meta:
        verbose_name = "Mouse Log"
        verbose_name_plural = "Mouse Logs"

    def __str__(self):
        return f"{self.user} - {self.action} at ({self.x_coordinate}, {self.y_coordinate}) on {self.timestamp}"
