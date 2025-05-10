from cms.models import AboutUs  
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item, Cart
from django.urls import reverse
from django.views import View
from django.utils import timezone
from random import shuffle
from notifications.models import Review
from recom.utils import get_recommendations
from .models import Order
from Payment.models import RentalPlan
from django.contrib.auth import logout
from cms.models import JobPosting, CompanyCulture, Benefit
from django.shortcuts import render
from django.http import JsonResponse
from .forms import ContactForm
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.utils import timezone
from .models import Item

def home(request):
    current_date = timezone.now().date()  # Use .date() to compare with DateField

    # Exclude items that are currently booked (active rental plans within start_date and end_date)
    items = Item.objects.filter(status='Approved').exclude(
        rentalplan__is_active=True,
        rentalplan__start_date__lte=current_date,
        rentalplan__end_date__gte=current_date
    )

    # Get all unique categories for sidebar
    categories = Item.objects.values_list('category', flat=True).distinct()

    context = {
        'items': items,
        'categories': categories,
        'current_date': current_date,
    }
    return render(request, 'index.html', context)

def category_items(request, category):
    current_date = timezone.now().date()
    # Filter items by category and exclude those with active rentals
    items = Item.objects.filter(category__iexact=category).exclude(
        rentalplan__is_active=True,
        rentalplan__start_date__lte=current_date,
        rentalplan__end_date__gte=current_date
    )
    
    # Get all unique categories for sidebar
    categories = Item.objects.values_list('category', flat=True).distinct()
    
    return render(request, 'index.html', {
        'items': items,
        'category': category,
        'categories': categories,
    })
def product_desc(request, product_id):
    # Get the current product
    item = get_object_or_404(Item, pk=product_id)

   
    related_items = list(Item.objects.filter(
        category=item.category, location=item.location
    ).exclude(pk=product_id))  

   
    shuffle(related_items)
    related_items = related_items[:4]

    context = {
        'item': item,
        'related_items': related_items,
    }

    return render(request, 'product_desc.html', context)



def filtered_items(request):
    selected_location = request.GET.get('location', '')
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    items = Item.objects.all()

    if selected_location:
        items = items.filter(location__iexact=selected_location)

    if query:
        items = items.filter(name__icontains=query)

    if category:
        items = items.filter(category__iexact=category)

    # Get all unique categories for sidebar
    categories = Item.objects.values_list('category', flat=True).distinct()

    return render(request, 'index.html', {
        'items': items,
        'selected_location': selected_location,
        'query': query,
        'category': category,
        'categories': categories,
    })






def get_cart_item_count(user):
    """Returns the number of items in the cart for the authenticated user."""
    return Cart.objects.filter(user=user).count() if user.is_authenticated else 0



def item_detail(request, id):
    item = Item.objects.get(id=id)
    recommended_items = get_recommendations(item_id=id, num_recommendations=4)
    related_items = Item.objects.filter(category=item.category).exclude(id=id)[:4]
    reviews = Review.objects.filter(item=item, approved=True)
 
    cart_item_count = get_cart_item_count(request.user)
    
    context = {
        'item': item,
        'recommended_items': recommended_items,
        'related_items': related_items,
        'reviews': reviews,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'product_desc.html', context)



@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{item.name} has been added to your cart.")
    return redirect('cart')



@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.item.price * item.quantity for item in cart_items)
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })



@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    new_quantity = int(request.POST.get('quantity', 1))
    
    if new_quantity > 0:
        cart_item.quantity = new_quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    messages.success(request, "Your cart has been updated.")
    return redirect('cart')



@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    
    messages.success(request, "Item has been removed from your cart.")
    return redirect('cart')


@login_required
def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    messages.success(request, "Your cart has been cleared.")
    return redirect('cart')


@login_required
def proceed_to_checkout(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    checkout_url = reverse('checkout', kwargs={'item_id': cart_item.item.id})
    redirect_url = f"{checkout_url}?quantity={cart_item.quantity}"
    return redirect(redirect_url)


@login_required
def rental_dashboard(request):
    # Fetch rental history (items rented by the user)
    rental_history = Item.objects.filter(rentalplan__renter=request.user).distinct()
    
    # Fetch all payments made by the user
    payments = RentalPlan.objects.filter(renter=request.user, is_active=True)
    
    # Calculate total payment amount
    total_payment = sum(payment.amount_due for payment in payments)
    
    # Note: The 'order' variable from your original code is unused in the template,
    # so I'm omitting it unless you need it for something specific.
    
    return render(request, 'rental_dashboard.html', {
        'rental_history': rental_history,
        'payments': payments,
        'total_payment': total_payment,
})
    

def about_us(request):
    about = AboutUs.objects.first()  
    if not about:
        about = AboutUs()  
    return render(request, 'aboutus.html', {'about': about})


def careers(request):
    jobs = JobPosting.objects.filter(is_active=True)
    culture_items = CompanyCulture.objects.all()  
    benefits = Benefit.objects.all()  

    context = {
        'jobs': jobs,
        'culture_items': culture_items,
        'benefits': benefits,
    }
    return render(request, 'careers.html', context)



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
    
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., save to database or send email)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Example: Save to a model or send an email (implement as needed)
            # Contact.objects.create(name=name, email=email, message=message)
            return JsonResponse({'status': 'success', 'message': 'Thank you for your message!'})
        else:
            return JsonResponse({'status': 'error', 'error': 'Invalid form data.'}, status=400)
    else:
        form = ContactForm()
    return render(request, 'contact-us.html', {'form': form})