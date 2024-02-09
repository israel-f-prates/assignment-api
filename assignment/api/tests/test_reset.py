from rest_framework import status
from rest_framework.test import APITestCase

class TestReset(APITestCase):
    def test_http_200(self):
        """The /reset endpoint must always return 200."""
        response = self.client.post('/reset')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_is_deleted(self):
        """Test whether a single account has been deleted after reset."""
        response = self.client.post('/event', {'type' : 'deposit', 'destination' : '100', 'amount' : 10})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/balance?account_id=100')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/reset')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/balance?account_id=100')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_accounts_are_deleted(self):
        """Test whether multiple accounts have been deleted after reset."""
        response = self.client.post('/event', {'type' : 'deposit', 'destination' : '100', 'amount' : 10})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/event', {'type' : 'deposit', 'destination' : '101', 'amount' : 20})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/event', {'type' : 'deposit', 'destination' : '102', 'amount' : 30})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/balance?account_id=100')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/balance?account_id=101')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/balance?account_id=102')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/reset')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/balance?account_id=100')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get('/balance?account_id=101')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get('/balance?account_id=102')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
