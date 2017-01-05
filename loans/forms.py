from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from loans.models import Loan


class LoanForm(forms.ModelForm):
    amount = forms.DecimalField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'step': '0.01',
                'min': Loan.MIN_AMOUNT / 100,
                'max': Loan.MAX_AMOUNT / 100,
                'type': 'number',
            }
        )
    )

    end_date = forms.DateField(
        required=True,
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Loan
        fields = ['amount', 'reason', 'end_date']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        # Because money values are normally stored in pence
        amount = float(amount)
        amount = amount * 100
        amount = int(amount)
        if amount < Loan.MIN_AMOUNT:
            raise ValidationError('Loan too small')

        if amount > Loan.MAX_AMOUNT:
            raise ValidationError('Loan too big')

        return amount

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        if end_date <= date.today():
            raise ValidationError('Loan must be paid back in the future')

        return end_date
