
from django.test import TestCase
from django.contrib.auth.models import User

from core.settings import DEFAULT_BALANCE


class Tests(TestCase):

    def test_account_balance_creation(self):
        """
        Test new users receive the default account balance.
        """
        user = User.objects.create(username="test")
        self.assertEquals(DEFAULT_BALANCE, user.account.balance)

    def test_view(self):
        """
        General test for the main view to ensure it loads.
        """
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)
