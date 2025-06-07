from django.db import models

# Create your models here.
class Payment(models.Model):
    status = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gateway_reference = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(blank)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    
