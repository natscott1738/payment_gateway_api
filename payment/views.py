from django.shortcuts import render
from .models import Payment
from rest_framework.views import  APIView
from django.conf import settings
import random
import string
from rest_framework import status
from rest_framework.response import Response
from .serializers import PaymentSerializer
from paystackapi.transaction import Transaction

# Create your views here.
class initiate_payment(APIView):
    def post(self, request, *args, **kwargs):
        
        # converting the payment object into JSON
        serializer = PaymentSerializer(data=request.data)

        # validating the serializer
        if serializer.is_valid():
            payment = serializer.save()

            # generating a payment reference
            ref = 'PYT-' + ''.join(random.choices(string.ascii_uppercase+string.digits, k=10))

            # API wrapper for paystack
            response = Transaction.initialize(
                name=payment.customer_name,
                email=payment.customer_email,
                amount=int(payment.payment_amount*100),
                reference=ref,
                callback='https://yourdomain.com/payment/callback'
            )

            # checking if payment request was succesful
            if response['status']:
                payment.gateway_reference = ref
                payment.save()

                return Response({
                    'status': 'success',
                    'authorization_url': response['data']['authorization_url']
                }, status=status.HTTP_201_CREATED)
            return Response({'error': 'Payment failed!'}, status=400)
        return Response(serializer.errors, status=400)
    
class PaymentStatusView(APIView):
    def get(self, request, payment_id, *args, **kwargs):
        try:
            payment=Payment.objects.get(id=payment_id)
            serializer = PaymentSerializer(payment)
            return Response({
                'status': 'Success',
                'message': 'payment details retrieved',
                'payment': serializer.data
            }, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'retrieval failure'
            }, status=status.HTTP_400_BAD_REQUEST)