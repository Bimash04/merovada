from django.shortcuts import render,redirect
from .models import AboutUs, TeamMember,ContactSubmission
from django.contrib import messages
from django.core.mail import send_mail
def about_us(request):
    about_us = AboutUs.objects.first()  
    team_members = TeamMember.objects.all()  
    if not about_us:
        about_us = AboutUs.objects.create()  
    return render(request, 'aboutus.html', {
        'about_us': about_us,
        'team_members': team_members
    })


def contact_support(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Save to database
        ContactSubmission.objects.create(name=name, email=email, message=message)
        
        messages.success(request, 'Thank you for your submission! We’ll get back to you soon.')
        return redirect('help_centre')
    return redirect('help_centre')   

def contact_support_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
      
        send_mail(
            subject=f'Contact Support from {name}',
            message=message,
            from_email=email,
            recipient_list=['bimash.dulal.logicseed@gmail.com'],  
            fail_silently=False,
        )
        
        messages.success(request, 'Thank you for your submission! We’ll get back to you soon.')
        return redirect('help_centre')
    return redirect('help_centre')


def secure_payment(request):
    return render(request, 'secure-payments.html')

def quantity(request):
    return render(request, 'quality-control.html')

def easy_return(request):
    return render(request, 'easy-returns.html')


def free_delivery(request):
    return render(request, 'free-delivery.html')