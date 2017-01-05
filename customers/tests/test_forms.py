from unittest.mock import patch

from django.test import TestCase, RequestFactory

from customers.forms import PhoneNumberVerifyForm, CompanyDetailsConfirmForm


class TestPhoneNumberVerifyForm(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_validation(self):
        form_data = {'verify_token': '1234'}
        form = PhoneNumberVerifyForm(data=form_data)
        form.request = self.factory.post('')
        form.request.session = {'verify_token': '0000'}
        form.is_valid()
        assert form.errors['__all__'], 'Error was not thrown'

        form_data = {'verify_token': '0000'}
        form = PhoneNumberVerifyForm(data=form_data)
        form.request = self.factory.post('')
        form.request.session = {'verify_token': '0000'}
        form.is_valid()
        assert not form.errors.get('__all__'), 'Error was thrown'


class TestCompanyDetailsConfirmForm(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('customers.forms.requests.get')
    def test_validation_company_found(self, get):
        form_data = {
            'registered_company_number': '12345678',
            'business_sector': 'PROFESSIONAL_SERVICES',
        }

        # Set API response code
        get.return_value.status_code = 200

        form = CompanyDetailsConfirmForm(data=form_data)
        form.is_valid()
        assert not form.errors.get('__all__'), 'Error was thrown'

    @patch('customers.forms.requests.get')
    def test_validation_company_not_found(self, get):
        form_data = {
            'registered_company_number': '12345678',
            'business_sector': 'PROFESSIONAL_SERVICES',
        }

        # Set API response code
        get.return_value.status_code = 404

        form = CompanyDetailsConfirmForm(data=form_data)
        form.is_valid()
        assert form.errors['__all__'], 'Error was not thrown'
