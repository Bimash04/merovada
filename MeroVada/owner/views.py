from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.conf import settings
from .models import Item
from .forms import ItemForm, ItemImageFormSet
from datetime import timedelta
from django.utils import timezone
from renter.models import Booking,Cart,Order
from notifications.models import Notification,Review
from Payment.models import RentalPlan
from Register.models import CustomUser


@login_required
@user_passes_test(lambda u: u.is_staff)  
def pending_items(request):
    """View to display pending items for admin approval."""
    items = Item.objects.filter(status='Pending')
    return render(request, 'pending_items.html', {'items': items})

@login_required
@user_passes_test(lambda u: u.is_staff)  # Only allow admin users
def approve_item(request, item_id):
    """Approve an item and notify the owner via email."""
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
       
        item.save()
        # Send email to owner upon approval
        send_mail(
            'Your Item Has Been Approved',
            f'Your item titled "{item.name}" has been approved and is now visible on the dashboard.',
            'bimash.dulal.logicseed@gmail.com',  
            [item.owner.email],
            fail_silently=False,
        )
        return redirect('admin_dashboard')
    return render(request, 'approve_item.html', {'item': item})

@login_required
@user_passes_test(lambda u: u.is_staff)  
def reject_item(request, item_id):
    """Reject an item and notify the owner via email."""
    item = get_object_or_404(Item, id=item_id)
    item.status = 'Rejected'
    item.save()
    send_email(item, "Rejected")
    messages.error(request, f'Item "{item.name}" rejected.')
    return redirect('pending_items')

@login_required
@user_passes_test(lambda u: u.is_staff)  
def update_status(request, item_id, status):
    """Update the status of an item to a valid status."""
    item = get_object_or_404(Item, id=item_id)
    if status in [choice[0] for choice in Item.STATUS_CHOICES]:
        item.status = status
        item.save()
        messages.success(request, f'Item "{item.name}" status updated to {status}.')
    else:
        messages.error(request, 'Invalid status update.')
    return redirect('dashboard')

# ------------------- Email Helper -------------------

def send_email(item, status):
    """Helper function to send email notifications."""
    try:
        send_mail(
            subject=f'Item {status}',
            message=f'Your item "{item.name}" has been {status.lower()}.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[item.owner.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending email: {e}")

# ------------------- Owner Views -------------------


@login_required
def add_item(request):
    """Add a new item to the inventory."""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        formset = ItemImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            
            formset.instance = item
            formset.save()

            return redirect('owner_dashboard')
    else:
        form = ItemForm()
        formset = ItemImageFormSet()
    
    return render(request, 'add_item.html', {'form': form, 'formset': formset})


@login_required
def list_items(request):
    """List items owned by the logged-in user."""
    items = Item.objects.filter(owner=request.user).order_by('-created_at')
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list_items.html', {'page_obj': page_obj})

@login_required
def edit_item(request, item_id):
    """Edit an existing item."""
    item = get_object_or_404(Item, id=item_id, owner=request.user)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('list_items')
    else:
        form = ItemForm(instance=item)

    return render(request, 'edit_item.html', {'form': form, 'item': item})

@login_required
def delete_item(request, item_id):
    """Delete an item owned by the logged-in user."""
    item = get_object_or_404(Item, id=item_id, owner=request.user)

    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('list_items')

    return render(request, 'delete_item.html', {'item': item})

# ------------------- Renter Views -------------------

def dashboard(request):
    """Dashboard for renters to browse items based on filters."""
    status_filter = request.GET.get('status', 'All')
    category_filter = request.GET.get('category', 'All')

    items = Item.objects.all()
    if status_filter != 'All':
        items = items.filter(status=status_filter)
    if category_filter != 'All':
        items = items.filter(category=category_filter)

    return render(request, 'dashboard.html', {
        'items': items,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'status_choices': Item.STATUS_CHOICES,
        'category_choices': Item.CATEGORY_CHOICES,
    })


@login_required
def owner_dashboard(request):
    # Fetch items owned by the logged-in user
    items = Item.objects.filter(owner=request.user)
    total_items = items.count()
    approved_items = items.filter(status='Approved').count()
    pending_items = items.filter(status='Pending').count()
    rejected_items = items.filter(status='Rejected').count()

   
    context = {
        'items': items,
        'total_items': total_items,
        'approved_items': approved_items,
        'pending_items': pending_items,
        'rejected_items': rejected_items,
    }

    return render(request, 'owner_dashboard.html', context)
