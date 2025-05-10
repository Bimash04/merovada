from django.db import models
from django.conf import settings
from owner.models import Item

class RentalPlan(models.Model):
    PAYMENT_FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('fortnightly', 'Fortnightly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('half_yearly', 'Half-Yearly'),
        ('yearly', 'Yearly'),
    ]

    renter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_frequency = models.CharField(max_length=20, choices=PAYMENT_FREQUENCY_CHOICES)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    last_payment_date = models.DateField(null=True, blank=True)
    next_payment_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.renter.username} - {self.item.name} ({self.payment_frequency})"
