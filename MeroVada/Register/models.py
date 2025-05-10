from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Custom User model
class CustomUser(AbstractUser):
    OWNER = 'owner'
    RENTER = 'renter'

    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (RENTER, 'Renter'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=RENTER)
    email_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.username


# Profile model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    verification_token = models.UUIDField(default=None, null=True, blank=True)




@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

