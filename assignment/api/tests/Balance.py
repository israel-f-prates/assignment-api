from rest_framework import status
from rest_framework.test import APITestCase

class BalanceTests(APITestCase):
    deposit_data = { 'type' : 'deposit', 'destination' : '100', 'amount' : 100 }

    def test_existing_account(self):
        """Balance must be returned for existing account."""
        response = self.client.post('/event', self.deposit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(f'/balance?account_id=100')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), 100)

    def test_non_existing_account(self):
        """Balance should return zero and HTTP 404 for non-existing account."""
        response = self.client.get(f'/balance?account_id=100')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), 0)

    def test_balance_without_filter(self):
        """Balance should reject requests without filtering."""
        response = self.client.get(f'/balance')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #self.assertEqual(response.json(), 0)
