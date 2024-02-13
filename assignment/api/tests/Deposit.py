from rest_framework import status
from rest_framework.test import APITestCase

class DepositTests(APITestCase):
    deposit_data = { 'type' : 'deposit', 'destination' : '100', 'amount' : 100 }

    def test_new_account(self):
        """Depositing to a non-existing account should create a new account."""
        expected_data = { 'destination' : { 'id' : '100', 'balance' : 100 } }
        response = self.client.post('/event', self.deposit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), expected_data)

    def test_existing_account(self):
        """Depositing to an existing account should update its balance."""
        expected_data = { 'destination' : { 'id' : '100', 'balance' : 200 } }
        response = self.client.post('/event', self.deposit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/event', self.deposit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), expected_data)

    def test_missing_payload(self):
        """Requests without payload should be rejected."""
        response = self.client.post('/event')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_malformed_content(self):
        """Requests with malformed content should be rejected."""
        malformed_data = [
            { 'destination' : '100', 'amount' : 100 }, # Missing type.
            { 'type' : 'deposit', 'amount' : 100 }, # Missing destination.
            { 'type' : 'deposit', 'destination' : '100' }, # Missing amount.
            { 'type' : 'does_not_exist', 'destination' : '100', 'amount' : 100 }, # Invalid type.
            { 'type' : 'deposit', 'destination' : '100', 'amount' : -100 }, # Invalid amount.
        ]
        for data in malformed_data:
            response = self.client.post('/event', data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
