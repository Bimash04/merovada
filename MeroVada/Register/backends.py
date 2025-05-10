from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class EmailVerifiedBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password) and user.email_verified:
                return user
        except CustomUser.DoesNotExist:
            return None
