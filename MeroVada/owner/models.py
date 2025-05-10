from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

class Item(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    CATEGORY_CHOICES = [
        ('Room', 'Room'),
        ('Apartment', 'Apartment'),
        ('Flat', 'Flat'),
        ('Furniture', 'Furniture'),
        ('Bike', 'Bike'),
        ('Car', 'Car'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=150, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    image = models.ImageField(upload_to='item_images/', null=True, blank=True)
    video = models.FileField(upload_to='item_videos/', null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users', null=True)
    
   
    def __str__(self):
        return self.name

    def clean(self):
        # Ensure that at least one image is uploaded
        if not self.image:
            raise ValidationError("You must upload at least 1 image for the item.")
    
    def save(self, *args, **kwargs):
        
        self.clean()
        super().save(*args, **kwargs)
        
class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='item_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.item.name}"