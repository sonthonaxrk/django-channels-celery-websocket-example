import json

from unittest.mock import patch
from django.test import TestCase
from twilio import TwilioRestException

from customers.models import Customer
from customers.tasks import send_phone_code


def create_message_factory(throw=False):
    def create_message(*args, **kwargs):
        if throw:
            raise TwilioRestException(500, '/')

    return create_message


class TestTwilloTask(TestCase):
    @patch('customers.tasks.Group')
    @patch('customers.tasks.TwilioRestClient')
    @patch('customers.tasks.sleep')
    def test_send_phone_code_success(
        self, sleep, twillo_client_factory, group
    ):
        customer = Customer.objects.create(username='testname')
        twillo_client_factory().messages.create = create_message_factory(False)
        send_phone_code(customer.id, '1234', '0412345678')
        assert group.call_args[0][0] == 'phone_verify-testname'
        sent_data = json.loads(group().send.call_args[0][0]['text'])
        assert sent_data['success'] == True

    @patch('customers.tasks.Group')
    @patch('customers.tasks.TwilioRestClient')
    @patch('customers.tasks.sleep')
    def test_send_phone_code_failure(
        self, sleep, twillo_client_factory, group
    ):
        customer = Customer.objects.create(username='testname')
        twillo_client_factory().messages.create = create_message_factory(True)
        send_phone_code(customer.id, '1234', '0412345678')
        assert group.call_args[0][0] == 'phone_verify-testname'
        sent_data = json.loads(group().send.call_args[0][0]['text'])
        assert sent_data['success'] == False
