from unittest.mock import patch
from django.test import TestCase, RequestFactory

from django.core.urlresolvers import reverse

from customers.models import Customer
from customers.views import ProfileBasic


class TestProfileViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('customers.views.messages')
    def test_profile_basic(self, m):
        customer = Customer.objects.create(username='testname')
        request = self.factory.post(reverse('account_basic_info'))
        request.user = customer
        request.POST['first_name'] = 'John'
        request.POST['last_name'] = 'Smith'

        response = ProfileBasic.as_view()(request)
        assert response.status_code == 302
        assert customer.first_name == 'John'
        assert customer.last_name == 'Smith'
