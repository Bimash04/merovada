from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CustomUserRegistrationForm
from .models import  Profile
import uuid
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .forms import ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Deactivate account until email is verified
            user.is_active = False  
            user.save()
            
            # Generate verification link
            verification_token = str(uuid.uuid4())
            user.profile.verification_token = verification_token
            user.profile.save()
            verification_link = request.build_absolute_uri(reverse('verify_email', args=[verification_token]))

            # Send email with verification link
            send_mail(
                'Verify Your Email',
                f'Click the link to verify your email: {verification_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return render(request, 'email_sent.html')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'register.html', {'form': form})



class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        # Display an error message if the form is invalid (e.g., incorrect username or password)
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

    def form_valid(self, form):
        login(self.request, form.get_user())
        user = form.get_user()
        # Check user role and redirect to respective dashboard
        if user.role == 'owner':
            return redirect('owner_dashboard')  
        elif user.role == 'renter':
            return redirect('home')  
        return redirect('home')  



def verify_email(request, token):
    try:
        profile = Profile.objects.get(verification_token=token)
        user = profile.user
        user.is_active = True
        user.email_verified = True
        user.save()
        profile.verification_token = None
        profile.save()

        # Send login link after successful verification
        login_url = request.build_absolute_uri(reverse('login'))  
        send_mail(
            'Login to Your Account',
            f'Your email has been verified successfully. Click here to login: {login_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return render(request, 'verified.html') 
    except Profile.DoesNotExist:
        return HttpResponse("Invalid or expired token.")




@login_required
def profile_view(request):
    return render(request, 'profile.html', {'profile': request.user.profile})

def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'profile_update.html', {'form': form})


@login_required
def profile_delete(request):
    request.user.profile.delete()
    return redirect('home')
