from .views import initiate_payment, PaymentStatusView
from django.urls import path

urlpatterns = [
    path('payments', initiate_payment.as_view(), name='initiate-payment'),
    path('payments/<int:payment_id>', PaymentStatusView.as_view(), name='payment-status')
]