from unittest.mock import patch

from django.test import TestCase, RequestFactory

from customers.models import Customer
from customers.views import profile_basic, profile_phone_number
from django.urls import reverse


class TestProfileViews(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch('customers.views.messages')
    def test_profile_basic(self, mock_messages):
        customer = Customer.objects.create()
        request = self.factory.post('')
        request.user = customer
        request.POST['first_name'] = 'Test'
        profile_basic(request)
        import pdb
        pdb.set_trace()

        customer = Customer.objects.create()
        request = self.factory.post('')
        request.user = customer
        request.POST['first_name'] = 'Test'
        request.POST['last_name'] = 'Name'
        profile_basic(request)

        assert customer.first_name == 'Test'
        assert customer.last_name == 'Name'
        assert mock_messages.add_message.called, 'Messages were not called'

    @patch('customers.views._send_phone_code')
    def test_profile_set_phone_number(self, _send_phone_code):
        customer = Customer.objects.create()
        request = self.factory.post('')
        request.user = customer
        request.POST['phone_number'] = '441234567890'
        response = profile_phone_number(request)

        assert customer.phone_number == '441234567890'
        assert customer.confirmed_phone_number is False
        assert customer.phone_number_confirmation_code
        assert len(customer.phone_number_confirmation_code) == 4
        assert customer.phone_number_confirmation_code.isdigit()
        assert _send_phone_code.called
        assert response.url == reverse('account_phone_number_verify')
