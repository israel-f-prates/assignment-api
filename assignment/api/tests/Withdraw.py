from rest_framework import status
from rest_framework.test import APITestCase

class WithdrawTests(APITestCase):
    deposit_data = { 'type' : 'deposit', 'destination' : '100', 'amount' : 100 }
    withdraw_data = { 'type' : 'withdraw', 'origin' : '100', 'amount' : 50 }

    def test_non_existing_account(self):
        """Withdrawing from a non-existing account should fail."""
        response = self.client.post('/event', self.withdraw_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_existing_account(self):
        """Withdrawing from an existing account with balance should succeed."""
        response = self.client.post('/event', self.deposit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/event', self.withdraw_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_existing_account_no_balance(self):
        """Withdrawing from an existing account without balance should fail."""
        response = self.client.post('/event', self.deposit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/event', self.withdraw_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/event', self.withdraw_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/event', self.withdraw_data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_missing_payload(self):
        """Requests without payload should be rejected."""
        response = self.client.post('/event')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_malformed_content(self):
        """Requests with malformed content should be rejected."""
        malformed_data = [
            { 'origin' : '100', 'amount' : 100 }, # Missing type.
            { 'type' : 'withdraw', 'amount' : 100 }, # Missing destination.
            { 'type' : 'withdraw', 'origin' : '100' }, # Missing amount.
            { 'type' : 'does_not_exist', 'origin' : '100', 'amount' : 100 }, # Invalid type.
            { 'type' : 'withdraw', 'origin' : '100', 'amount' : -100 }, # Invalid amount.
        ]
        for data in malformed_data:
            response = self.client.post('/event', data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
