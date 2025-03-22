from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User, BankAccountType, UserBankAccount, UserAddress


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = [
            'street_address',
            'city',
            'postal_code',
            'country'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })


class UserRegistrationForm(UserCreationForm):
    account_type = forms.ModelChoiceField(
        queryset=BankAccountType.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': (
                'appearance-none block w-full bg-gray-200 text-gray-700 '
                'border border-gray-200 rounded py-3 px-4 leading-tight '
                'focus:outline-none focus:bg-white focus:border-gray-500'
            )
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field != 'account_type':  # Already styled above
                self.fields[field].widget.attrs.update({
                    'class': (
                        'appearance-none block w-full bg-gray-200 text-gray-700 '
                        'border border-gray-200 rounded py-3 px-4 leading-tight '
                        'focus:outline-none focus:bg-white focus:border-gray-500'
                    )
                })

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserBankAccount.objects.create(
                user=user,
                account_type=self.cleaned_data['account_type'],
                account_no=user.id + settings.ACCOUNT_NUMBER_START_FROM
            )
        return user
