from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from .models import Payment

class PaymentAPITests(APITestCase):

    @patch('payment.views.Transaction.initialize')  # <- make sure this path matches your project
    def test_initiate_payment(self, mock_initialize):
        # Mock Paystack response
        mock_initialize.return_value = {
            "status": True,
            "data": {
                "authorization_url": "https://paystack.mock/redirect"
            }
        }

        url = reverse('initiate-payment')
        data = {
            "customer_name": "Alice",
            "customer_email": "alice@example.com",
            "payment_amount": 100.00
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('authorization_url', response.data)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(Payment.objects.first().customer_name, 'Alice')

    def test_retrieve_payment_status(self):
        # First, create a payment
        payment = Payment.objects.create(
            customer_name="Bob",
            customer_email="bob@example.com",
            payment_amount=75.00
        )
        url = reverse('payment-status', args=[payment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Success')
        self.assertEqual(response.data['payment']['customer_name'], 'Bob')

    def test_retrieve_nonexistent_payment(self):
        url = reverse('payment-status', args=[999])  # Non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'failed')  # <- Update to match your view logic