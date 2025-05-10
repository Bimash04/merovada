# cms/admin/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from Register.models import CustomUser
from owner.models import Item
from renter.models import Order
from notifications.models import Notification,Review
from Payment.models import RentalPlan
from Blog.models import BlogPost
from chat.models import ChatMessage
from notifications.models import Notification
from renter.models import  Booking, Cart
from cms.models import ContactSubmission
from django import forms
# cms/admin/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from Register.models import CustomUser, Profile
from owner.models import Item, ItemImage
from renter.models import  Cart, Order, Booking
from notifications.models import Notification
from django import forms

# Forms for each model
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'category', 'location', 'status', 'image', 'video']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.Select(),
            'status': forms.Select(),
        }

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'email_verified', 'is_staff']
        widgets = {
            'role': forms.Select(),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'is_approved']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['notification_type', 'message', 'is_read']
        widgets = {
            'notification_type': forms.Select(),
            'message': forms.Textarea(attrs={'rows': 4}),
        }

class RentalPlanForm(forms.ModelForm):
    class Meta:
        model = RentalPlan
        fields = ['start_date', 'end_date', 'payment_frequency', 'amount_due', 'last_payment_date', 'next_payment_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'last_payment_date': forms.DateInput(attrs={'type': 'date'}),
            'next_payment_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_frequency': forms.Select(),
        }

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'total_price', 'shipping_address', 'payment_method', 'status']
        widgets = {
            'status': forms.Select(),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'status']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

# Dashboard view
@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    total_users = CustomUser.objects.count()
    total_items = Item.objects.count()
    total_orders = Order.objects.count()
    total_reviews = Review.objects.count()
    total_notifications = Notification.objects.count()
    total_rental_plans = RentalPlan.objects.count()
    total_carts = Cart.objects.count()
    total_bookings = Booking.objects.count()

    today = timezone.now()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    weekly_users = CustomUser.objects.filter(date_joined__gte=week_ago).count()
    monthly_users = CustomUser.objects.filter(date_joined__gte=month_ago).count()

    recent_items = Item.objects.all().order_by('-created_at')[:5]

    browser_stats = {
        'Google Chrome': 50,
        'Mozilla Firefox': 30,
        'Internet Explorer': 10,
        'Safari': 10,
    }

    traffic_types = {
        'Organic': 44.46,
        'Referral': 5.54,
        'Other': 50,
    }

    context = {
        'total_users': total_users,
        'total_items': total_items,
        'total_orders': total_orders,
        'total_reviews': total_reviews,
        'total_notifications': total_notifications,
        'total_rental_plans': total_rental_plans,
        'total_carts': total_carts,
        'total_bookings': total_bookings,
        'weekly_users': weekly_users,
        'monthly_users': monthly_users,
        'recent_items': recent_items,
        'browser_stats': browser_stats,
        'traffic_types': traffic_types,
    }
    return render(request, 'dashboard.html', context)

# Item CRUD
@login_required
def manage_items(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    all_items = Item.objects.all()
    return render(request, 'manage_items.html', {'all_items': all_items})

@login_required
def create_item(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, 'Item created successfully!')
            return redirect('manage_items')
        else:
            messages.error(request, 'Error creating item. Please check the form.')
    else:
        form = ItemForm()

    return render(request, 'create_item.html', {'form': form})

@login_required
def update_item(request, item_id):
    if not request.user.is_staff:
        return redirect('admin_login')

    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('manage_items')
        else:
            messages.error(request, 'Error updating item. Please check the form.')
    else:
        form = ItemForm(instance=item)

    return render(request, 'update_item.html', {'form': form, 'item': item})

@login_required
def delete_item(request, item_id):
    if not request.user.is_staff:
        return redirect('admin_login')

    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('manage_items')

    return render(request, 'delete_item.html', {'item': item})




# CustomUser CRUD
@login_required
def manage_users(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    all_users = CustomUser.objects.all()
    return render(request, 'manage_users.html', {'all_users': all_users})

@login_required
def create_user(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password('defaultpassword')  # Set a default password
            user.save()
            messages.success(request, 'User created successfully!')
            return redirect('manage_users')
        else:
            messages.error(request, 'Error creating user. Please check the form.')
    else:
        form = CustomUserForm()

    return render(request, 'create_user.html', {'form': form})

@login_required
def update_user(request, user_id):
    if not request.user.is_staff:
        return redirect('admin_login')

    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('manage_users')
        else:
            messages.error(request, 'Error updating user. Please check the form.')
    else:
        form = CustomUserForm(instance=user)

    return render(request, 'update_user.html', {'form': form, 'user': user})

@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return redirect('admin_login')

    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('manage_users')

    return render(request, 'delete_user.html', {'user': user})

# Profile CRUD
@login_required
def manage_profiles(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    all_profiles = Profile.objects.all()
    return render(request, 'manage_profiles.html', {'all_profiles': all_profiles})

@login_required
def create_profile(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('manage_profiles')
        else:
            messages.error(request, 'Error creating profile. Please check the form.')
    else:
        form = ProfileForm()

    return render(request, 'create_profile.html', {'form': form})

@login_required
def update_profile(request, profile_id):
    if not request.user.is_staff:
        return redirect('admin_login')

    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('manage_profiles')
        else:
            messages.error(request, 'Error updating profile. Please check the form.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form, 'profile': profile})

@login_required
def delete_profile(request, profile_id):
    if not request.user.is_staff:
        return redirect('admin_login')

    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == 'POST':
        profile.delete()
        messages.success(request, 'Profile deleted successfully!')
        return redirect('manage_profiles')

    return render(request, 'delete_profile.html', {'profile': profile})

# Review CRUD
@login_required
def manage_reviews(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    all_reviews = Review.objects.all()
    return render(request, 'manage_reviews.html', {'all_reviews': all_reviews})

# @login_required
# def create_review(request):
#     if not request.user.is_staff:
#         return redirect('admin_login')

#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Review created successfully!')
#             return redirect('manage_reviews')
#         else:
#             messages.error(request, 'Error creating review. Please check the form.')
#     else:
#         form = ReviewForm()

#     return render(request, 'create_review.html', {'form': form})

@login_required
def update_review(request, review_id):
    if not request.user.is_staff:
        return redirect('admin_login')

    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('manage_reviews')
        else:
            messages.error(request, 'Error updating review. Please check the form.')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'update_review.html', {'form': form, 'review': review})

@login_required
def delete_review(request, review_id):
    if not request.user.is_staff:
        return redirect('admin_login')

    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('manage_reviews')

    return render(request, 'delete_review.html', {'review': review})

# Notification CRUD
@login_required
def manage_notifications(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    all_notifications = Notification.objects.all()
    return render(request, 'manage_notifications.html', {'all_notifications': all_notifications})

# @login_required
# def create_notification(request):
#     if not request.user.is_staff:
#         return redirect('admin_login')

#     if request.method == 'POST':
#         form = NotificationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Notification created successfully!')
#             return redirect('manage_notifications')
#         else:
#             messages.error(request, 'Error creating notification. Please check the form.')
#     else:
#         form = NotificationForm()

#     return render(request, 'create_notification.html', {'form': form})

# @login_required
# def update_notification(request, notification_id):
#     if not request.user.is_staff:
#         return redirect('admin_login')

#     notification = get_object_or_404(Notification, id=notification_id)
#     if request.method == 'POST':
#         form = NotificationForm(request.POST, instance=notification)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Notification updated successfully!')
#             return redirect('manage_notifications')
#         else:
#             messages.error(request, 'Error updating notification. Please check the form.')
#     else:
#         form = NotificationForm(instance=notification)

#     return render(request, 'update_notification.html', {'form': form, 'notification': notification})

# @login_required
# def delete_notification(request, notification_id):
#     if not request.user.is_staff:
#         return redirect('admin_login')

#     notification = get_object_or_404(Notification, id=notification_id)
#     if request.method == 'POST':
#         notification.delete()
#         messages.success(request, 'Notification deleted successfully!')
#         return redirect('manage_notifications')

#     return render(request, 'delete_notification.html', {'notification': notification})




def careers(request):
    return render(request, 'careeers.html')
# RentalPlan CRUD
@login_required
def manage_rental_plans(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    all_rental_plans = RentalPlan.objects.all()
    return render(request, 'manage_rental_plans.html', {'all_rental_plans': all_rental_plans})

# @login_required
# def create_rental_plan(request):
#     if not request.user.is_staff:
#         return redirect('admin_login')

#     if request.method == 'POST':
#         form = RentalPlanForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Rental plan created successfully!')
#             return redirect('manage_rental_plans')
#         else:
#             messages.error(request, 'Error creating rental plan. Please check the form.')
#     else:
#         form = RentalPlanForm()

#     return render(request, 'create_rental_plan.html', {'form': form})

# @login_required
# def update_rental_plan(request, rental_plan_id):
#     if not request.user.is_staff:
#         return redirect('admin_login')

#     rental_plan = get_object_or_404(RentalPlan, id=rental_plan_id)
#     if request.method == 'POST':
#         form = RentalPlanForm(request.POST, instance=rental_plan)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Rental plan updated successfully!')
#             return redirect('manage_rental_plans')
#         else:
#             messages.error(request, 'Error updating rental plan. Please check the form.')
#     else:
#         form = RentalPlanForm(instance=rental_plan)

#     return render(request, 'update_rental_plan.html', {'form': form, 'rental_plan': rental_plan})

# @login_required
# def delete_rental_plan(request, rental_plan_id):
#     if not request.user.is_staff:
#         return redirect('admin_login')

#     rental_plan = get_object_or_404(RentalPlan, id=rental_plan_id)
#     if request.method == 'POST':
#         rental_plan.delete()
#         messages.success(request, 'Rental plan deleted successfully!')
#         return redirect('manage_rental_plans')

#     return render(request, 'delete_rental_plan.html', {'rental_plan': rental_plan})

# Cart CRUD
# @login_required
# def manage_carts(request):
#     if not request.user.is_staff:
#         return redirect('admin_login')

#     all_carts = Cart.objects.all()
#     return render(request, 'manage_carts.html', {'all_carts': all_carts})

# @login_required
# def create_cart(request):
#     if not request.user.is_staff:
#         return redirect('admin_login')

#     if request.method == 'POST':
#         form = CartForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Cart created successfully!')
#             return redirect('manage_carts')
#         else:
#             messages.error(request, 'Error creating cart. Please check the form.')
#     else:
#         form = CartForm()

#     return render(request, 'create_cart.html', {'form': form})

# @login_required
# def update_cart(request, cart_id):
#     if not request.user.is_staff:
#         return redirect('admin_login')

#     cart = get_object_or_404(Cart, id=cart_id)
#     if request.method == 'POST':
#         form = CartForm(request.POST, instance=cart)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Cart updated successfully!')
#             return redirect('manage_carts')
#         else:
#             messages.error(request, 'Error updating cart. Please check the form.')
#     else:
#         form = CartForm(instance=cart)

#     return render(request, 'update_cart.html', {'form': form, 'cart': cart})

# @login_required
# def delete_cart(request, cart_id):
#     if not request.user.is_staff:
#         return redirect('admin_login')

#     cart = get_object_or_404(Cart, id=cart_id)
#     if request.method == 'POST':
#         cart.delete()
#         messages.success(request, 'Cart deleted successfully!')
#         return redirect('manage_carts')

#     return render(request, 'delete_cart.html', {'cart': cart})

# Order CRUD
@login_required
def manage_orders(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    all_orders = Order.objects.all()
    return render(request, 'manage_orders.html', {'all_orders': all_orders})

@login_required
def create_order(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order created successfully!')
            return redirect('manage_orders')
        else:
            messages.error(request, 'Error creating order. Please check the form.')
    else:
        form = OrderForm()

    return render(request, 'create_order.html', {'form': form})

@login_required
def update_order(request, order_id):
    if not request.user.is_staff:
        return redirect('admin_login')

    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order updated successfully!')
            return redirect('manage_orders')
        else:
            messages.error(request, 'Error updating order. Please check the form.')
    else:
        form = OrderForm(instance=order)

    return render(request, 'update_order.html', {'form': form, 'order': order})

@login_required
def delete_order(request, order_id):
    if not request.user.is_staff:
        return redirect('admin_login')

    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order deleted successfully!')
        return redirect('manage_orders')

    return render(request, 'delete_order.html', {'order': order})

# Booking CRUD
@login_required
def manage_bookings(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    all_bookings = Booking.objects.all()
    return render(request, 'manage_bookings.html', {'all_bookings': all_bookings})

# @login_required
# def create_booking(request):
#     if not request.user.is_staff:
#         return redirect('admin_login')

#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Booking created successfully!')
#             return redirect('manage_bookings')
#         else:
#             messages.error(request, 'Error creating booking. Please check the form.')
#     else:
#         form = BookingForm()

#     return render(request, 'create_booking.html', {'form': form})

# @login_required
# def update_booking(request, booking_id):
#     if not request.user.is_staff:
#         return redirect('admin_login')

#     booking = get_object_or_404(Booking, id=booking_id)
#     if request.method == 'POST':
#         form = BookingForm(request.POST, instance=booking)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Booking updated successfully!')
#             return redirect('manage_bookings')
#         else:
#             messages.error(request, 'Error updating booking. Please check the form.')
#     else:
#         form = BookingForm(instance=booking)

#     return render(request, 'update_booking.html', {'form': form, 'booking': booking})

# @login_required
# def delete_booking(request, booking_id):
#     if not request.user.is_staff:
#         return redirect('admin_login')

#     booking = get_object_or_404(Booking, id=booking_id)
#     if request.method == 'POST':
#         booking.delete()
#         messages.success(request, 'Booking deleted successfully!')
#         return redirect('manage_bookings')

#     return render(request, 'delete_booking.html', {'booking': booking})

# Authentication views
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or not an admin user')
    return render(request, 'admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models import JobPosting
from ..form import JobPostingForm,CompanyCultureForm,BenefitForm,AboutUsForm

# Restrict to superusers only
@login_required
@user_passes_test(lambda u: u.is_superuser)
def post_job(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('careers')
    else:
        form = JobPostingForm()
    
    return render(request, 'post_job.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_culture(request):
    if request.method == 'POST':
        form = CompanyCultureForm(request.POST, request.FILES)  # Added request.FILES for image upload
        if form.is_valid():
            form.save()
            return redirect('careers')
    else:
        form = CompanyCultureForm()
    return render(request, 'add_culture.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_benefit(request):
    if request.method == 'POST':
        form = BenefitForm(request.POST, request.FILES)  # Added request.FILES for image upload
        if form.is_valid():
            form.save()
            return redirect('careers')
    else:
        form = BenefitForm()
    return render(request, 'add_benefit.html', {'form': form})


from ..models import AboutUs
@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_about_us(request):
    if AboutUs.objects.exists():
        return redirect('edit_about_us')  # Redirect to edit if content already exists

    if request.method == 'POST':
        form = AboutUsForm(request.POST, request.FILES)  # Include request.FILES for image
        if form.is_valid():
            form.save()
            return redirect('about_us')
    else:
        form = AboutUsForm()
    return render(request, 'add_about_us.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_about_us(request):
    about = AboutUs.objects.first()
    if not about:
        return redirect('add_about_us')  # Redirect to add if no content exists

    if request.method == 'POST':
        form = AboutUsForm(request.POST, request.FILES, instance=about)
        if form.is_valid():
            form.save()
            return redirect('about_us')
    else:
        form = AboutUsForm(instance=about)
    return render(request, 'edit_about_us.html', {'form': form})