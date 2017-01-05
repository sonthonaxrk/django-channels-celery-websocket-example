import requests

from functools import lru_cache

from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from customers.models import Customer, Company


class UserDetailsConfirmForm(forms.ModelForm):
    """
    These details may be prepopulated with the Oauth
    Scope Data
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.confirm_button_text = 'Confirm'

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', ]


class PhoneNumberVerifyForm(forms.Form):
    verify_token = forms.CharField(
        label="Verification code",
        required=True, max_length=4
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.confirm_button_text = 'Verify Phone Number'

    def clean(self):
        cleaned_data = super().clean()
        verify_token = cleaned_data.get('verify_token')

        if verify_token != self.request.session['verify_token']:
            raise ValidationError('Incorrect Validation Code')

        return cleaned_data


class PhoneNumberConfirmForm(forms.ModelForm):
    phone_number = forms.CharField(
        label="Phone number (+44123456789)",
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.confirm_button_text = 'Confirm'

    def clean(self):
        cleaned_data = super().clean()
        new_phone_number = self.cleaned_data.get('phone_number')
        if new_phone_number == self.instance.phone_number:
            raise ValidationError('Old Phone Number Entered')

        return cleaned_data


    class Meta:
        model = Customer
        fields = ['phone_number', ]


class CompanyDetailsConfirmForm(forms.ModelForm):
    """
    This form takes a registered_company_number and
    fetches additional information from the companieshouse
    API and saves it onto the model.
    """
    class Meta:
        model = Company
        fields = [
            'registered_company_number', 'business_sector',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.confirm_button_text = 'Confirm'

    # Why is there an LRU cache?
    #
    # This is called by the clean method first to verify the existance
    # of the company. Subsequently it is called again by the save method
    # to save additional details about the company.
    @lru_cache(maxsize=None)
    def _get_company_details(self, company_number):
        endpoint = 'https://api.companieshouse.gov.uk/company/{}'.format(
            company_number
        )

        auth = (settings.COMPANIES_HOUSE_API_KEY, '')

        company_details = requests.get(endpoint, auth=auth)

        if company_details.status_code != 200:
            raise ValidationError('Company not found')

        return company_details.json()

    def save(self, *args, **kwargs):
        company_details = self._get_company_details(
            self.cleaned_data['registered_company_number']
        )

        address = company_details.get('registered_office_address', {})
        self.instance.name = company_details.get('company_name')
        self.instance.address_line_1 = address.get('address_line_1')
        self.instance.address_line_2 = address.get('address_line_2')
        self.instance.country = address.get('country')
        self.instance.postal_code = address.get('postal_code')

        return super().save(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        # Raises an error if the company doesn't exist
        self._get_company_details(cleaned_data['registered_company_number'])
        return cleaned_data


class CompanyDetailsVerifyForm(forms.ModelForm):
    """
    Sub form used to populate the company details
    verify form
    """
    class Meta:
        model = Company
        fields = []
