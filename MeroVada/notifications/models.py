from django.db import models
from django.conf import settings
from owner.models import Item

class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    def __str__(self):
        return f"Review by {self.user.username} on {self.item.name}"
    
    

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('review', 'Review'),
        ('message', 'Message'),
        ('alert', 'Alert'),
    ]
    review = models.ForeignKey(
        'Review', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

    def mark_as_read(self):
        self.is_read = True
        self.save